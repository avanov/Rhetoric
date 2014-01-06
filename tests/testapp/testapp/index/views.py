from rhetoric import view_config


@view_config(route_name='index.dashboard', renderer='index.html')
def dashboard(request):
    return {}
