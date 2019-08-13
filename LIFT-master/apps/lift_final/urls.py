from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^workouts$', views.workouts),
    url(r'^register$', views.register),
    url(r'^info$', views.info),
    url(r'^input$', views.input),
    url(r'^home$', views.home),
    url(r'^login$', views.login),
    url(r'^log_out$', views.log_out),
    url(r'^workouts$', views.workouts),
    url(r'^(?P<workout_id>\d+)/info$', views.workout_info),
    url(r'^(?P<user_id>\d+)/profile$', views.profile),
    url(r'^(?P<user_id>\d+)/update$', views.update),
    url(r'^(?P<workout_id>\d+)/my_workout$', views.my_workout),
    url(r'^(?P<workout_id>\d+)/remove_workout$', views.remove_workout),
]