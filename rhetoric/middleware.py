from rhetoric.view import ViewCallback

class UrlResolverMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if not isinstance(callback, ViewCallback):
            return

        callback.resolve_actual_view_callable(request, callback_args, callback_kwargs)
