from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^add$', views.add),
    url(r'^addItem$', views.addItem),
    url(r'^wishItems/(?P<id>\d+)$', views.wishItems),
    url(r'^addToMyWishes/(?P<id>\d+)$', views.addToMyWishes),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^removeWish/(?P<id>\d+)$', views.removeWish),
    url(r'^$', views.index),
]
