from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.map, name='map'),
    url(r'^beginingstory$', views.beginingstory, name="beginingstory"),
    # url(r'^task\d*$', views.beginingstory, name="task"),
    url(r'^task2/$', views.task2, name="task2"),
    url(r'^task1/task1_question1/$', views.task1_question1, name="task1_question1"),
    url(r'^task1/task1_question2/$', views.task1_question2, name="task1_question2"),
]
