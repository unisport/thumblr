from django.conf.urls import patterns, url, include
from django.contrib import admin

from thumblr import urls as thumblr_urls

urlpatterns = patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^thumblr/', include(thumblr_urls, namespace='thumblr')),
    )