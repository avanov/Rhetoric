from collections import OrderedDict
import inspect

import pkg_resources
import venusian

from rhetoric.config.rendering import RenderingConfiguratorMixin
from rhetoric.config.rendering import BUILTIN_RENDERERS
from rhetoric.config.routes import RoutesConfiguratorMixin
from rhetoric.config.views import ViewsConfiguratorMixin
from rhetoric.path import caller_package
from rhetoric.exceptions import ConfigurationError
from rhetoric.view import view_config
from rhetoric.url import route_path, create_django_route


__all__ = ['route_path', 'view_config', 'Configurator']


class Configurator(
    RoutesConfiguratorMixin,
    ViewsConfiguratorMixin,
    RenderingConfiguratorMixin):

    venusian = venusian
    inspect = inspect

    def __init__(self, route_prefix=None):
        if route_prefix is None:
            route_prefix = ''
        self.route_prefix = route_prefix

        self.routes = OrderedDict()
        self.renderers = {}

        self.setup_registry()

    def include(self, callable, route_prefix=None):
        if route_prefix is None:
            route_prefix = ''

        old_route_prefix = self.route_prefix
        route_prefix = u'{}/{}'.format(old_route_prefix.rstrip('/'), route_prefix.lstrip('/'))
        self.set_route_prefix(route_prefix)

        c = self.maybe_dotted(callable)
        module = self.inspect.getmodule(c)
        if module is c:
            try:
                c = getattr(module, 'includeme')
            except AttributeError:
                raise ConfigurationError(
                    "module {} has no attribute 'includeme'".format(module.__name__)
                )

        sourcefile = self.inspect.getsourcefile(c)

        if sourcefile is None:
            raise ConfigurationError(
                'No source file for module {} (.py file must exist, '
                'refusing to use orphan .pyc or .pyo file).'.format(module.__name__)
            )

        c(self)
        self.set_route_prefix(old_route_prefix)

    def django_urls(self):
        """Converts registered routes to a list of Django URLs"""
        return [
            create_django_route(
                name=route_dict['name'],
                pattern=route_dict['pattern'],
                rules=route_dict.get('rules'),
                extra_kwargs=route_dict.get('extra_kwargs'),
                viewlist=route_dict['viewlist']
            )
            for route_dict in self.routes.values()
        ]

    def scan(self, package=None, categories=None, onerror=None, ignore=None):
        if package is None:
            package = caller_package()

        scanner = self.venusian.Scanner(config=self)
        scanner.scan(package, categories=categories, onerror=onerror, ignore=ignore)
        self.check_consistency()

    def setup_registry(self):
        # Add default renderers
        # ---------------------
        for name, renderer in BUILTIN_RENDERERS.items():
            self.add_renderer(name, renderer)

    def check_consistency(self):
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

    def maybe_dotted(self, dotted):
        if not isinstance(dotted, str):
            return dotted
        return self._pkg_resources_style(dotted)

    def _pkg_resources_style(self, value):
        """
        This method is taken from Pyramid Web Framework.
        package.module:attr style
        """
        return pkg_resources.EntryPoint.parse('x={}'.format(value)).load(False)

    def set_route_prefix(self, prefix):
        self.route_prefix = prefix
