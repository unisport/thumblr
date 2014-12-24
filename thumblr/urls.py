from django.conf.urls import patterns, include, url
from django.contrib import admin
from thumblr import views


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sizes/$', views.imagesizes, name='imagesizes'),
)
