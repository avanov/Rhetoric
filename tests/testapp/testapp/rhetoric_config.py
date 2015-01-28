# Rhetorical routing
# ------------------
import operator
from pkg_resources import parse_version

from rhetoric import Configurator
from rhetoric.config.util import as_sorted_tuple
from tests.testapp.testapp.blog import includeme as blog_config


class ApiVersionPredicate(object):
    OPERATORS = {
        '>': operator.gt,
        '<': operator.lt,
        '==': operator.eq,
        '>=': operator.ge,
        '<=': operator.le
    }
    def __init__(self, val, config):
        """
        :param val: value passed to view_config/view_defaults
        :param config:
        """
        api_version = as_sorted_tuple(val)
        self.val = api_version

    def text(self):
        return u'api_version = {}'.format(self.val)

    phash = text

    def __call__(self, context, request):
        """
        :param context: at the moment context may be only None
        :type context: None
        :param: request: Django request object
        :type request: :class:`django.http.HttpRequest`
        """
        for allowed_api_pattern in self.val:
            if self.match_api_version(request.META['X-API-VERSION'], allowed_api_pattern):
                return True
        return False

    def match_api_version(self, request_version, allowed_version):
        """

        :param request_version:
        :param allowed_version: may be represented in following forms:
            1. ``VERSION``
            2. ``==VERSION`` (the same as above)
            3. ``>VERSION``
            4. ``<VERSION``
            5. ``>=VERSION``
            6. ``<=Version``
            7. Comma-separated list of 1-7 evaluated as AND
        :return: :raise ValueError:
        """
        distinct_versions = {version.strip() for version in allowed_version.split(',')}
        for distinct_version in distinct_versions:
            operation = self.OPERATORS.get(distinct_version[:2])
            if operation:
                # prepare cases #2, #5, #6
                compare_with = distinct_version[2:]
            else:
                operation = self.OPERATORS.get(distinct_version[0])
                if operation:
                    # prepare cases #3, #4
                    compare_with = distinct_version[1:]
                else:
                    # prepare case #1
                    compare_with = distinct_version
                    operation = self.OPERATORS['==']

            # evaluate the case
            matched = operation(parse_version(request_version), parse_version(compare_with))
            if not matched:
                return False
        return True


class ValidateFormPredicate(object):
    def __init__(self, val, config):
        """

        :param val: 2-tuple of ('request_attribute_name', FormValidator)
        :type val: tuple
        :param config:
        :return:
        """
        self.val = val

    def text(self):
        return u'validate_form = {}'.format(self.val)

    phash = text

    def __call__(self, context, request):
        form_data = getattr(request, self.val[0])
        form = self.val[1](form_data)
        return form.is_valid()


config = Configurator()
config.add_view_predicate('api_version', ApiVersionPredicate)
config.add_view_predicate('validate_form', ValidateFormPredicate)

config.include('tests.testapp.testapp.index')
config.include(blog_config, '/blog')
config.include('tests.testapp.testapp.articles', '/articles')
