from rhetoric.exceptions import ConfigurationError


class ViewsConfiguratorMixin(object):
    def add_view(self, view, route_name, renderer=None, request_method=None, decorator=None, check_csrf=False):
        try:
            route = self.routes[route_name]
        except KeyError:
            raise ConfigurationError(
                'No route named {route_name} found for view registration'.format(route_name=route_name)
            )

        def combine(*decorators):
            def decorated(view_callable):
                # reversed() is allows a more natural ordering in the api
                for decorator in reversed(decorators):
                    view_callable = decorator(view_callable)
                return view_callable
            return decorated

        if isinstance(decorator, tuple):
            decorator = combine(*decorator)

        if decorator:
            view = decorator(view)

        # csrf_exempt is used by Django CSRF Middleware
        view.csrf_exempt = not check_csrf
        route_item = {
            'view': view
        }

        if renderer is None:
            renderer = ''
        route_item['renderer'] = self.get_renderer(renderer)

        # Register predicates
        # -------------------------------------
        if request_method is None:
            request_method = {'GET'}
        elif isinstance(request_method, str):
            request_method = {request_method}
        request_method = set(request_method)

        route_item['predicates'] = {
            'request_method': request_method
        }
        route['viewlist'].append(route_item)
