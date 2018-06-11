from django.urls import path

from . import views

app_name = 'links'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('links/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('vote/', views.vote, name='vote'),
    path('slack/auth/', views.slack_oauth, name='oauth')
]