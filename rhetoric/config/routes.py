from rhetoric.exceptions import ConfigurationError


class RoutesConfiguratorMixin(object):
    def add_route(self, name, pattern, rules=None, extra_kwargs=None):
        pattern = u'{}/{}'.format(self.route_prefix.rstrip('/'), pattern.lstrip('/'))
        self.routes[name] = {
            'name': name,
            'pattern': pattern,
            'rules': rules,
            'extra_kwargs': extra_kwargs,
            'viewlist': [],
        }

    def check_routes_consistency(self):
        for route_name, route in self.routes.items():
            viewlist = route['viewlist']
            if not viewlist:
                raise ConfigurationError(
                    'Route name "{name}" is not associated with a view callable.'.format(name=route_name)
                )
            for route_item in viewlist:
                if route_item.get('view') is None:
                    raise ConfigurationError(
                        'Route name "{name}" is not associated with a view callable.'.format(name=route_name)
                    )
