import inspect
import functools


def viewdefaults(wrapped):
    """ This function is a copy of ``pyramid.util.viewdefaults``.

    Decorator for add_view-like methods which takes into account
    __view_defaults__ attached to view it is passed. Not a documented API but
    used by some external systems.
    """
    def wrapper(self, *arg, **kw):
        defaults = {}
        if arg:
            view = arg[0]
        else:
            view = kw.get('view')
        view = self.maybe_dotted(view)
        if inspect.isclass(view):
            defaults = getattr(view, '__view_defaults__', {}).copy()

        # We do not use action_method
        # Uncomment this when it's necessary
        # ----------------------------------
        #if not '_backframes' in kw:
        #    kw['_backframes'] = 1 # for action_method

        defaults.update(kw)
        return wrapped(self, *arg, **defaults)
    return functools.wraps(wrapped)(wrapper)
