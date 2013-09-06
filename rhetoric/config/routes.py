
class RoutesConfiguratorMixin(object):
    def add_route(self, name, pattern, rules=None, extra_kwargs=None):
        self.routes[name] = {
            'name': name,
            'pattern': pattern,
            'rules': rules,
            'extra_kwargs': extra_kwargs,
            'viewlist': [],
        }

    def get_route(self, name):
        return self.routes[name]
