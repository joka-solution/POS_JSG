from django.conf.urls import url, include
from django.contrib import admin
from .views import home_page, logout

#

urlpatterns = [
    url(r'^$', home_page, name='home_page'),
    url(r'^logout/$', logout, name='logout'),
]