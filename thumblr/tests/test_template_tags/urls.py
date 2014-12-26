from django.conf.urls import patterns, url
from thumblr.views import imagesizes

urlpatterns = patterns('',
    url(r'size_adding', imagesizes)
)