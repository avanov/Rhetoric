from rhetoric.config.util import as_sorted_tuple


class RequestMethodPredicate(object):
    def __init__(self, val, config):
        request_method = as_sorted_tuple(val)
        if 'GET' in request_method and 'HEAD' not in request_method:
            # GET implies HEAD too
            request_method = as_sorted_tuple(request_method + ('HEAD',))
        self.val = request_method

    def text(self):
        return 'request_method = %s' % (','.join(self.val))

    phash = text

    def __call__(self, context, request):
        return request.method in self.val