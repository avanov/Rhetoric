import re

from django.conf.urls import patterns, include, url
from django.contrib import admin

from rhetoric import Configurator


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)

# Rhetorical routing
# ------------------
config = Configurator()
config.add_route('test.new.routes', '/test/new/routes/{param:[a-z]+}')
config.scan(ignore=[
    # do not scan settings modules
    re.compile('^project_name.settings[_]?[_a-z09]*$').match,
])
urlpatterns.extend(config.django_urls())