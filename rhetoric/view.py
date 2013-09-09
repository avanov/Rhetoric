from django.core.urlresolvers import RegexURLPattern as DjangoRegexURLPattern
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
            scanner.config.add_view(view=wrapped, **settings)

        self.venusian.attach(wrapped, callback, category='rhetoric', depth=depth + 1)
        return wrapped


class ViewCallback(object):
    def __init__(self, viewlist):
        self.viewlist = viewlist

    def __call__(self, request, *args, **kwargs):
        view_settings = self.find_view_settings(request, args, kwargs)
        response = view_settings['view'](request, *args, **kwargs)
        return self.process_callback_response(request, response, view_settings)

    def find_view_settings(self, request, args, kwargs):
        if hasattr(request, 'rhetoric_view_settings'):
            return getattr(request, 'rhetoric_view_settings')

        for view_settings in self.viewlist:
            if self.check_predicates(view_settings['predicates'], request, args, kwargs):
                setattr(request, 'rhetoric_view_settings', view_settings)
                return view_settings
        raise Http404

    def check_predicates(self, predicates, request, req_args, req_kw):
        if request.method not in predicates['request_method']:
            return False
        return True

    def process_callback_response(self, request, response, view_settings):
        if isinstance(response, HttpResponse):
            # Do not process standard django responses
            return response
        renderer = view_settings['renderer']
        return renderer(request, response)


class RegexURLPattern(DjangoRegexURLPattern):
    def __init__(self, regex, default_args=None, name=None, viewlist=None):
        super(RegexURLPattern, self).__init__(regex, ViewCallback(viewlist), default_args, name)
        self.viewlist = viewlist
