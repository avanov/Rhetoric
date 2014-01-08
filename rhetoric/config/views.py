import inspect

from rhetoric.exceptions import ConfigurationError
from rhetoric.util import viewdefaults


class ViewsConfiguratorMixin(object):

    @viewdefaults
    def add_view(self,
                 view=None,
                 route_name=None,
                 request_method=None,
                 attr=None,
                 api_version=None,
                 decorator=None,
                 check_csrf=False,
                 renderer=None):
        """

        :param view: callable
        :param route_name:
        :type route_name: str or None
        :param request_method:
        :type request_method: str or tuple
        :param attr:
          This knob is most useful when the view definition is a class.

          The view machinery defaults to using the ``__call__`` method
          of the :term:`view callable` (or the function itself, if the
          view callable is a function) to obtain a response.  The
          ``attr`` value allows you to vary the method attribute used
          to obtain the response.  For example, if your view was a
          class, and the class has a method named ``index`` and you
          wanted to use this method instead of the class' ``__call__``
          method to return the response, you'd say ``attr="index"`` in the
          view configuration for the view.
        :type attr: str
        :param api_version:
        :type api_version: str or tuple
        :param decorator:
        :param check_csrf:
        :param renderer:
        :return: :raise ConfigurationError:
        """
        try:
            route = self.routes[route_name]
        except KeyError:
            raise ConfigurationError(
                'No route named {route_name} found for view registration'.format(route_name=route_name)
            )

        # Parse view
        # -----------------------------------------------
        if inspect.isclass(view):
            actual_method = attr if attr else '__call__'
            view = ClassViewWrapper(view, actual_method)

        # Add decorators
        # -----------------------------------------------
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
        # -----------------------------------------------
        view.csrf_exempt = not check_csrf

        # Register predicates
        # -------------------------------------
        if request_method is None:
            request_method = {'GET'}
        elif isinstance(request_method, str):
            request_method = {request_method}
        request_method = set(request_method)

        if api_version is not None:
            if isinstance(api_version, str):
                api_version = {api_version}
            api_version = set(api_version)

        # Renderers
        # -------------------------------------
        if renderer is None:
            renderer = 'string'

        # Save
        # -------------------------------------
        route_item = {
            'view': view,
            'attr': attr,
            'api_version_getter': self.api_version_getter,
            'renderer': self.get_renderer(renderer),
            'predicates': {
                'request_method': request_method,
                'api_version': api_version
                },
        }
        route['viewlist'].append(route_item)


class ClassViewWrapper(object):
    def __init__(self, view_class, method_to_call):
        self.view_class = view_class
        self.method_to_call = method_to_call

    def __call__(self, request, *args, **kw):
        instance = self.view_class(request, *args, **kw)
        view = getattr(instance, self.method_to_call)
        return view()
