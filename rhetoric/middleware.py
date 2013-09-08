from django.middleware.csrf import CsrfViewMiddleware

from rhetoric.view import ViewCallback


class CsrfProtectedViewDispatchMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if isinstance(callback, ViewCallback):
            view_settings = callback.find_view_settings(request, callback_args, callback_kwargs)
            # Check the actual view callable rather than ViewCallback wrapper with CsrfViewMiddleware
            return super(CsrfProtectedViewDispatchMiddleware, self).process_view(
                request, view_settings['view'], callback_args, callback_kwargs
            )

        # The callable is not a part of Rhetoric
        return super(CsrfProtectedViewDispatchMiddleware, self).process_view(
            request, callback, callback_args, callback_kwargs
        )