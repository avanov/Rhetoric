from django.core.urlresolvers import ResolverMatch, LocaleRegexProvider
from django.http import HttpResponse, Http404

import venusian


class view_config(object):
    venusian = venusian

    def __init__(self, **settings):
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(scanner, name, ob):
            wrapped.csrf_exempt = settings.pop('csrf_exempt', True)
            scanner.config.add_view(view=wrapped, **settings)

        self.venusian.attach(wrapped, callback, category='rhetoric', depth=depth + 1)
        return wrapped


class ViewCallback(object):
    def __init__(self, viewlist):
        self.viewlist = viewlist
        self.callback = None
        self.view_settings = None
        self.csrf_exempt = False

    def resolve_actual_view_callable(self, request, args, kwargs):
        for view_settings in self.viewlist:
            if self.check_predicates(view_settings['predicates'], request, args, kwargs):
                self.callback = view_settings['view']
                self.view_settings = view_settings
                self.csrf_exempt = self.callback.csrf_exempt
                return
        raise Http404

    def __call__(self, request, *args, **kwargs):
        response = self.callback(request, *args, **kwargs)
        return self.process_callback_response(response, self.view_settings)

    def check_predicates(self, predicates, request, req_args, req_kw):
        if request.method not in predicates['request_method']:
            return False
        return True

    def process_callback_response(self, response, view_settings):
        if isinstance(response, HttpResponse):
            # Do not process standard django responses
            return response
        renderer = view_settings['renderer']
        return renderer(response)


class RegexURLPattern(LocaleRegexProvider):
    def __init__(self, regex, default_args=None, name=None, viewlist=None):
        LocaleRegexProvider.__init__(self, regex)
        self.default_args = default_args or {}
        self.name = name
        self.viewlist = viewlist


    def resolve(self, path):
        match = self.regex.search(path)
        if match:
            # If there are any named groups, use those as kwargs, ignoring
            # non-named groups. Otherwise, pass all non-named arguments as
            # positional arguments.
            kwargs = match.groupdict()
            if kwargs:
                args = ()
            else:
                args = match.groups()
            # In both cases, pass any extra_kwargs as **kwargs.
            kwargs.update(self.default_args)

            callback = ViewCallback(self.viewlist)
            return ResolverMatch(callback, args, kwargs, self.name)
