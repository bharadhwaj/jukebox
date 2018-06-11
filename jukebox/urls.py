from django.urls import path

from . import views

app_name = 'links'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('vote/', views.VoteView.as_view(), name='vote'),
    path('votes/', views.vote, name='votes'),
]