from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


json_encode = DjangoJSONEncoder().encode


class JsonRendererFactory(object):
    def __init__(self, name):
        """ Constructor: info will be an object having the the
        following attributes: name (the renderer name), package
        (the package that was 'current' at the time the
        renderer was registered), type (the renderer type
        name), registry (the current application registry) and
        settings (the deployment settings dictionary).  """
        self.name = name

    def __call__(self, value, system=None):
        """ Call a the renderer implementation with the value
        and the system value passed in as arguments and return
        the result (a string or unicode object).  The value is
        the return value of a view.  The system value is a
        dictionary containing available system values
        (e.g. view, context, and request). """
        return HttpResponse(json_encode(value), content_type='application/json; charset=utf-8')


DEFAULT_RENDERERS = {
    'json': JsonRendererFactory,
    'string': lambda data: HttpResponse(data,
                                        content_type='text/plain; charset=utf-8'),
}


class RenderingConfiguratorMixin(object):

    def add_renderer(self, name, factory):
        self.renderers[name] = factory

    def get_renderer(self, name):
        if '.' in name:
            # template-based renderer
            _unused_part_, renderer_name = name.rsplit('.', 1)
        else:
            renderer_name = name

        try:
            return self.renderers[renderer_name](name)
        except KeyError:
            raise ValueError('No such renderer factory {}'.format(renderer_name))
