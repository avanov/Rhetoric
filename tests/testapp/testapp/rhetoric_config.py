# Rhetorical routing
# ------------------
from rhetoric import Configurator
from tests.testapp.testapp.blog import includeme as blog_config


config = Configurator()
api_getter = lambda request: request.META['X-API-VERSION']
config.set_api_version_getter(api_getter)

config.include('tests.testapp.testapp.index')
config.include(blog_config, '/blog')
config.include('tests.testapp.testapp.articles')
