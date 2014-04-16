import re

from django.conf.urls import patterns, include, url
from django.contrib import admin

from rhetoric import Configurator

from tests.testapp.testapp.blog import includeme as blog_config


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

# Rhetorical routing
# ------------------
from .rhetoric_config import config
urlpatterns.extend(config.django_urls())
