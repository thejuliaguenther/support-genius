from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tickets/$', views.tickets, name='tickets'),
    url(r'^one_ticket/$', views.one_ticket, name='one_ticket'),  #update to pull ticket id 
]