from django.views.decorators.http import require_http_methods

from rhetoric import view_config


@view_config(route_name='index.dashboard', request_method='GET', renderer='index.html')
def dashboard(request):
    return {'method': 'GET'}


# request method restrictions using django decorators (for testing Rhetoric's "decorator" option)

@view_config(route_name='index.dashboard', request_method='POST', renderer='index.html',
             # only POST method will be handled, since the request_method param
             # is explicitly set
             decorator=require_http_methods(["GET", "POST"]))
def post_on_dashboard(request):
    return {'method': 'POST'}
