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
api_getter = lambda request: request.META['X-API-VERSION']

config = Configurator()
config.set_api_version_getter(api_getter)
config.include('tests.testapp.testapp.index')
config.include(blog_config, '/blog')
config.scan(ignore=[
    # do not scan settings modules
    re.compile('^project_name.settings[_]?[_a-z09]*$').match,
])
urlpatterns.extend(config.django_urls())
