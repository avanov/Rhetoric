from django.http import HttpResponse
from rhetoric import view_config


@view_config(route_name='test.new.routes')
def default_view(request, param):
    return {}


@view_config(route_name='test.new.routes', request_method='POST')
def submit_form_view(request):
    return {}


@view_config(route_name='test.new.routes', request_method='POST', api_version='1.0')
def api_v1_submit_form_view(request):
    return {}


@view_config(route_name='blog.page', request_method='GET', renderer='json')
def blog_page(request, page_slug):
    # test custom response status api
    request.response.status_code = 201
    return {
        'page_slug': page_slug
    }


@view_config(route_name='blog.page', request_method='POST', renderer='json')
def blog_page_post(request, page_slug):
    return HttpResponse(page_slug)
