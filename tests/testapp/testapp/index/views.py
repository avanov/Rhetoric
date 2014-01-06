from rhetoric import view_config


@view_config(route_name='index.dashboard')
def dashboard(request):
    return {}
