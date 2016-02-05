from django.conf.urls import url
from . import views

app_name = 'wp'
urlpatterns = [
    url(r'^add$', views.add, name='index'),
    url(r'^lookup$', views.lookup, name='lookup'),
]