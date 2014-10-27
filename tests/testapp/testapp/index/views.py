from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET, require_POST

from rhetoric import view_config
from rhetoric import view_defaults


def phony_decorator(view):
    """ Decorator for testing Rhetoric's decorator predicate.
    """
    def decorated(request, *args, **kwargs):
        return view(request, *args, **kwargs)
    return decorated


@view_config(route_name='index.dashboard', request_method='GET', renderer='index.html')
def dashboard(request):
    return {'method': 'GET'}


# request method restrictions using django decorators (for testing Rhetoric's "decorator" option)

@view_config(route_name='index.dashboard', request_method='POST', renderer='index.html',
             # only POST method will be handled, since the request_method param
             # is explicitly set
             decorator=require_http_methods(["GET", "POST"]))
def post_on_dashboard(request):
    request.response.status_code = 201
    return {'method': 'POST'}


@view_config(route_name='index.dashboard', request_method='PUT', renderer='index.html',
             # test multiple decorators combined
             decorator=(phony_decorator, phony_decorator))
def put_on_dashboard(request):
    return {'method': 'PUT'}


# Versioned views
# --------------------------------
@view_config(route_name='index.versions', request_method='GET', api_version='1.0', renderer='json')
def get_version_1(request):
    return {
        'version': '1.0'
    }

@view_config(route_name='index.versions', request_method='GET', api_version='>1.0, <2.0', renderer='json')
def get_version_1_range(request):
    return {
        'method': 'GET',
        'version': '>1.0, <2.0'
    }

@view_config(route_name='index.versions', request_method='POST', api_version='>1.0, <2.0', renderer='json')
def post_version_1_range(request):
    return {
        'method': 'POST',
        'version': '>1.0, <2.0'
    }

@view_config(route_name='index.versions', request_method='POST', api_version='>=2.0', renderer='json')
def post_version_2_range(request):
    return {
        'version': '>=2.0'
    }


@view_defaults(route_name='index.dashboard.api', renderer='json', api_version='>=1.0, <2.0')
class DashboardAPIv1(object):

    def __init__(self, request, *args, **kw):
        self.request = request

    @view_config(request_method='GET')
    def get_dashboard_items(self):
        return {
            'version': 1,
            'method': 'GET'
        }

    @view_config(request_method='POST')
    def post_dashboard_items(self):
        return {
            'version': 1,
            'method': 'POST'
        }


@view_defaults(route_name='index.dashboard.api', renderer='json', api_version='>=2.0')
class DashboardAPIv2(object):

    def __init__(self, request, *args, **kw):
        self.request = request

    @view_config(request_method='GET')
    def get_dashboard_items(self):
        return {
            'version': 2,
            'method': 'GET'
        }

    @view_config(request_method='POST')
    def post_dashboard_items(self):
        return {
            'version': 2,
            'method': 'POST'
        }

@view_config(route_name='index.json_body', request_method='POST', renderer='json')
def json_body(request):
    data = request.json_body
    if data:
        if 'key' in data:
            return {'result': 'key'}
    return {'result': 'no-key'}
