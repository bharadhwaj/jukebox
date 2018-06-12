import re
import os
import requests

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.conf import settings
from slackclient import SlackClient
from datetime import datetime

from .models import Link

class IndexView(generic.ListView):

    template_name = 'index.html'
    context_object_name = 'video_details'

    def initiate_slack(self):
        """ Initiate the slack method and returns the object"""
        slack_token  = os.environ['SLACK_TOKEN']
        return SlackClient(slack_token)
        
    def get_channel_id(self, sc, channel_name):
        """ Returns slack channel ID if name is provided """
        channels   = sc.api_call('channels.list')
        channel_id = None
        for channel in channels['channels']:
            if channel['name'] == channel_name:
                return(channel['id'])
        if channel_id == None:
            raise Exception("Error: Cannot find channel: " + channel_name)
    
    def find_youtube_links(self, sc, channel):
        """ Returns the Youtube links posted in the specified channel for last 7 days """
        url_regex = (r'((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?>')
        time_to   = datetime.now().timestamp()
        time_from = time_to - 604800
        key       = getattr(settings, 'API_KEY', None)
        urls_arr  = []

        history   = sc.api_call('channels.history', channel=channel, oldest=time_from, latest=time_to)
        if history and history['messages']:
            for message in history['messages']:
                youtube_urls = re.findall(url_regex, message['text'])
                if youtube_urls:
                    for url in youtube_urls:
                        r = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id=%s&key=%s' %(url[4], key))
                        response = r.json()
                        name = response['items'][0]['snippet']['title']
                        urls_arr.append({ 'url' : ''.join(url), 'video_id': url[4], 'name' : name })
                        
        return urls_arr
    
    def add_urls_to_database(self, url_array):
        """ Add the url array to database """
        urls_obj_arr = []
        for obj in url_array:
            urls_obj_arr.append(Link.objects.get_or_create(url=obj['url'], name=obj['name'], video_id=obj['video_id']))
        return urls_obj_arr

    def get_queryset(self):
        """Return the links ordered by votes and the playlist URL."""
        sc           = self.initiate_slack()
        channel_name = getattr(settings, 'SLACK_CHANNEL', None)
        channel_id   = self.get_channel_id(sc, channel_name)
        youtube_urls = self.find_youtube_links(sc, channel_id)
        urls_obj     = self.add_urls_to_database(youtube_urls)
        yt_urls      = Link.objects.order_by('-votes')
        yt_link_arr  = []
        for i in range(1,len(yt_urls)):
            yt_link_arr.append(yt_urls[i].video_id)
        playlist    = 'https://www.youtube.com/embed/%s?playlist=%s' %(yt_urls[0].video_id, ','.join(yt_link_arr))
        return { 'urls_list' : yt_urls, 'playlist' : playlist }

class VoteView(generic.ListView):

    template_name = 'votes/votes.html'
    context_object_name = 'urls_list'

    def get_queryset(self):
        """Return the links ordered by id."""
        indexObj     = IndexView()
        sc           = indexObj.initiate_slack()
        channel_name = getattr(settings, 'SLACK_CHANNEL', None)
        channel_id   = indexObj.get_channel_id(sc, channel_name)
        youtube_urls = indexObj.find_youtube_links(sc, channel_id)
        indexObj.add_urls_to_database(youtube_urls)
        return Link.objects.order_by('id')

class ResultView(generic.ListView):

    template_name = 'votes/result.html'
    context_object_name = 'urls_list'

    def get_queryset(self):
        """Return the links ordered by votes."""
        indexObj     = IndexView()
        sc           = indexObj.initiate_slack()
        channel_name = getattr(settings, 'SLACK_CHANNEL', None)
        channel_id   = indexObj.get_channel_id(sc, channel_name)
        youtube_urls = indexObj.find_youtube_links(sc, channel_id)
        indexObj.add_urls_to_database(youtube_urls)
        return Link.objects.order_by('-votes')


def vote(request):
    urls_list = Link.objects.all()
    try:
        voted_id     = request.POST['urls']
        selected_url = urls_list.get(pk=voted_id)
    except (KeyError, Link.DoesNotExist):
        messages.warning(request, 'Please choose any album and then submit.')
        return HttpResponseRedirect(reverse('links:vote'))

    else:
        selected_url.votes += 1
        selected_url.save()
        messages.success(request, 'Your have voted for ' + selected_url.name + '.')
        return HttpResponseRedirect(reverse('links:result'))
