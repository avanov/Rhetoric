import re

from rhetoric.view import RegexURLPattern
from rhetoric.adt import ADTMeta
from django.core.urlresolvers import reverse


# A replacement marker in a pattern must begin with an uppercase or
# lowercase ASCII letter or an underscore, and can be composed only
# of uppercase or lowercase ASCII letters, underscores, and numbers.
# For example: a, a_b, _b, and b9 are all valid replacement marker names, but 0a is not.
ROUTE_PATTERN_OPEN_BRACES_RE = re.compile('(?P<start_brace>\{).*')
ROUTE_PATTERN_CLOSING_BRACES_RE = re.compile('\}.*')


def _extract_braces_expression(line, starting_braces_re, open_braces_re, closing_braces_re):
    """
    This function is taken from Plim package: https://pypi.python.org/pypi/Plim/

    :param line: may be empty
    :type line: str
    :param starting_braces_re:
    :param open_braces_re:
    :param closing_braces_re:
    """
    match = starting_braces_re.match(line)
    if not match:
        return None

    open_brace = match.group('start_brace')
    buf = [open_brace]
    tail = line[len(open_brace):]
    braces_counter = 1

    while tail:
        current_char = tail[0]
        if closing_braces_re.match(current_char):
            braces_counter -= 1
            buf.append(current_char)
            if braces_counter:
                tail = tail[1:]
                continue
            return u''.join(buf), tail[1:]

        if open_braces_re.match(current_char):
            braces_counter += 1
            buf.append(current_char)
            tail = tail[1:]
            continue

        buf.append(current_char)
        tail = tail[1:]
    raise Exception("Unexpected end of a route definition: {}".format(line))


extract_pattern = lambda line: _extract_braces_expression(
    line,
    ROUTE_PATTERN_OPEN_BRACES_RE,
    ROUTE_PATTERN_OPEN_BRACES_RE,
    ROUTE_PATTERN_CLOSING_BRACES_RE
)


def create_django_route(name, pattern, rules=None, extra_kwargs=None, viewlist=None):
    """

    :param name: Route Name
    :type name: str
    :param pattern: URL pattern
    :type pattern: str
    :param rules:
    :type rules: dict
    :param extra_kwargs:
    :param viewlist:
    :return:
    """
    if rules is None:
        rules = {}
    # Django requires us to strip a prefixed slash
    pattern = pattern.lstrip('/')
    buf = []
    while pattern:
        result = extract_pattern(pattern)
        if result:
            result, pattern = result
            # Remove braces from the result "{pattern[:rule]}"
            result = result[1:-1]
            if ':' in result:
                # pattern in a "pattern_name:rule" form
                match_group_name, rule = result.split(':', 1)
            else:
                # pattern in a "pattern_name" form
                match_group_name = result
                rule = rules.get(match_group_name)
                if not rule:
                    # This default pattern is Pyramid's default.
                    rule = '[^/]+'
                elif isinstance(rule, ADTMeta):
                    # rule is an ADT
                    rule = u'(?:{})'.format(u'|'.join([str(v) for v in rule.values()]))

            result = u"(?P<{match_group_name}>{rule})".format(
                match_group_name=match_group_name,
                rule=rule
            )
            buf.append(result)
            continue

        buf.append(pattern[0])
        pattern = pattern[1:]

    # Parsing is done. Now join everything together
    buf = u''.join(buf)

    regex_pattern = u'^{expr}$'.format(expr=buf)
    return RegexURLPattern(regex_pattern, extra_kwargs, name, viewlist=viewlist)


def route_path(route_name, *elements, **kw):
    """

    :param route_name:
    :param elements:
    :param kw:
    :return:
    """
    return reverse(route_name, args=elements, kwargs=kw)
