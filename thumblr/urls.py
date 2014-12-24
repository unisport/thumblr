from django.conf.urls import patterns, include, url
from django.contrib import admin
from thumblr.views import imagesizes


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sizes/$', imagesizes, name='imagesizes'),
)
