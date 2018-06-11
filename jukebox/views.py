import time
import re
import os

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
    context_object_name = 'urls_list'

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
        urls_arr  = []

        history   = sc.api_call('channels.history', channel=channel, oldest=time_from, latest=time_to)
        if history and history['messages']:
            for message in history['messages']:
                youtube_urls = re.findall(url_regex, message['text'])
                if youtube_urls:
                    for url in youtube_urls:
                        urls_arr.append(''.join(url))
            
        return urls_arr
    
    def add_urls_to_database(self, url_array):
        """ Add the url array to database """
        urls_obj_arr = []
        for url in url_array:
            urls_obj_arr.append(Link.objects.get_or_create(url=url))
        return urls_obj_arr

    def get_queryset(self):
        """Return the links ordered by votes."""
        sc           = self.initiate_slack()
        channel_name = getattr(settings, 'SLACK_CHANNEL', None)
        channel_id   = self.get_channel_id(sc, channel_name)
        youtube_urls = self.find_youtube_links(sc, channel_id)
        urls_obj     = self.add_urls_to_database(youtube_urls)
        return Link.objects.order_by('-votes')

class DetailView(generic.DetailView):
    model = Link
    template_name = 'links/detail.html'

class ConfigureView(generic.DetailView):
    model = Link
    template_name = 'links/configure.html'

def vote(request):
    urls_list = Link.objects.all()
    try:
        selected_url = urls_list.get(pk=request.POST['urls'])
    except (KeyError, Link.DoesNotExist):
        messages.warning(request, 'Please choose any option')
        return HttpResponseRedirect(reverse('links:index'))

    else:
        selected_url.votes += 1
        selected_url.save()
        return HttpResponseRedirect(reverse('links:index'))
