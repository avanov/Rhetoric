from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render


json_encode = DjangoJSONEncoder().encode


class JsonRendererFactory(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, request, view_response):
        return HttpResponse(json_encode(view_response), content_type='application/json; charset=utf-8')


class StringRendererFactory(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, request, view_response):
        return HttpResponse(view_response, content_type='text/plain; charset=utf-8')


class DjangoTemplateRendererFactory(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, request, context_dict):
        return render(request, self.name, context_dict)


BUILTIN_RENDERERS = {
    'json': JsonRendererFactory,
    'string': StringRendererFactory,
    '.html': DjangoTemplateRendererFactory,
}


class RenderingConfiguratorMixin(object):

    def add_renderer(self, name, factory):
        self.renderers[name] = factory

    def get_renderer(self, name):
        try:
            template_suffix = name.rindex(".")
        except ValueError:
            # period is not found
            renderer_name = name
        else:
            renderer_name = name[template_suffix:]

        try:
            return self.renderers[renderer_name](name)
        except KeyError:
            raise ValueError('No such renderer factory {}'.format(renderer_name))
