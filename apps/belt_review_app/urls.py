from django.conf.urls import url
from . import views

#/users sends the register form
#"/login" sends the  login form

#this is the route for the create new list item
#<form action="/main" method="POST">

urlpatterns = [
######THESE ARE FOR RENDERING
#it starts at main
url(r'^main$', views.index),
#it then goes to the dashboard
url(r'^dashboard$', views.dashboard),
url(r'^wish_items/create$', views.additem),
url('^wish_items/add$', views.additem),
url('^wish_items/(?P<id>\d+)$', views.showuser),


	
######THESE ARE FOR ROUTES
#this will be the add new item route
url(r'^users$', views.register),
url(r'^addform$', views.addform),
###add and remove from wishlist
url('^(?P<id>\d+)/deletewish$', views.deletewish),
url('^(?P<id>\d+)/addwish$', views.addwish),
###process the form
url(r'^login$', views.login),
url(r'^logout$', views.logout)
]