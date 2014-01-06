from rhetoric import view_config


@view_config(route_name='test.new.routes')
def default_view(request):
    return {}
