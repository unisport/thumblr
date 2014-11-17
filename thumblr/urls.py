from django.conf.urls import patterns, url
from thumblr.views import add_image_view

urlpatterns = patterns('',
    url(r'^add_image/', add_image_view, name='add_image'),
)

