from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.conf import settings

from .models import Link

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'urls_list'

    def get_queryset(self):
        """Return the links."""
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

def slack_oauth(request):
    code = request.GET['code']
    
    params = { 
        'code': code,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    # Team.objects.create(
    #     name=data['name'], 
    #     team_id=data['team_id'],
    #     bot_user_id=data['bot']['bot_user_id'],     
    #     bot_access_token=data['bot']['bot_access_token']
    # )
    return HttpResponse('Bot added to your Slack team!')
