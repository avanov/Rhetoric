import inspect

import rhetoric.config.predicates
from rhetoric.exceptions import ConfigurationError
from rhetoric.util import viewdefaults


class ViewsConfiguratorMixin(object):

    @viewdefaults
    def add_view(self,
                 view=None,
                 route_name=None,
                 request_method=None,
                 attr=None,
                 decorator=None,
                 check_csrf=False,
                 renderer=None,
                 **predicates):
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
        :param decorator:
        :param check_csrf:
        :param renderer:
        :param predicates: Pass a key/value pair here to use a third-party predicate
                           registered via
                           :meth:`rhetoric.config.Configurator.add_view_predicate`.
                           More than one key/value pair can be used at the same time. See
                           :ref:`view_and_route_predicates` for more information about
                           third-party predicates.
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
            request_method = ('GET',)
        pvals = predicates.copy()
        pvals.update(
            dict(
                request_method=request_method,
                )
            )
        predlist = self.get_predlist('view')
        _weight_, preds, _phash_ = predlist.make(self, **pvals)

        # Renderers
        # -------------------------------------
        if renderer is None:
            renderer = 'string'

        # Save
        # -------------------------------------
        route_item = {
            'view': view,
            'attr': attr,
            'renderer': self.get_renderer(renderer),
            'predicates': preds,
        }
        route['viewlist'].append(route_item)

    def add_view_predicate(self, name, factory, weighs_more_than=None,
                           weighs_less_than=None):
        """
        Adds a view predicate factory.  The associated view predicate can
        later be named as a keyword argument to
        :meth:`rhetoric.config.Configurator.add_view` in the
        ``predicates`` anonymous keyword argument dictionary.

        ``name`` should be the name of the predicate.  It must be a valid
        Python identifier (it will be used as a keyword argument to
        ``add_view`` by others).

        ``factory`` should be a :term:`predicate factory` or :term:`dotted
        Python name` which refers to a predicate factory.

        See :ref:`view_and_route_predicates` for more information.
        """
        self._add_predicate(
            'view',
            name,
            factory,
            weighs_more_than=weighs_more_than,
            weighs_less_than=weighs_less_than
            )


    def add_default_view_predicates(self):
        p = rhetoric.config.predicates
        for name, factory in (
            ('request_method', p.RequestMethodPredicate),
            ):
            self.add_view_predicate(name, factory)


class ClassViewWrapper(object):
    def __init__(self, view_class, method_to_call):
        self.view_class = view_class
        self.method_to_call = method_to_call

    def __call__(self, request, *args, **kw):
        instance = self.view_class(request, *args, **kw)
        view = getattr(instance, self.method_to_call)
        return view()
