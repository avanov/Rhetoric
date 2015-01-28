from rhetoric.config.util import as_sorted_tuple


class RequestMethodPredicate(object):
    def __init__(self, val, config):
        """
        :param val: value passed to view_config/view_defaults
        :param config:
        """
        request_method = as_sorted_tuple(val)
        if 'GET' in request_method and 'HEAD' not in request_method:
            # GET implies HEAD too
            request_method = as_sorted_tuple(request_method + ('HEAD',))
        self.val = request_method

    def text(self):
        return 'request_method = %s' % (','.join(self.val))

    phash = text

    def __call__(self, context, request):
        """
        :param context: at the moment context may be only None
        :type context: None
        :param: request: Django request object
        :type request: :class:`django.http.HttpRequest`
        """
        return request.method in self.val
