from django.conf.urls import patterns, url
from thumblr.views import imagesizes


urlpatterns = patterns('',
                       url(r'^sizes/$', imagesizes, name='imagesizes'),
)
