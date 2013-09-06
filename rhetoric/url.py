import re

from rhetoric.view import RegexURLPattern
from django.core.urlresolvers import reverse


#A replacement marker in a pattern must begin with an uppercase or
# lowercase ASCII letter or an underscore, and can be composed only
# of uppercase or lowercase ASCII letters, underscores, and numbers.
# For example: a, a_b, _b, and b9 are all valid replacement marker names, but 0a is not.
ROUTE_PATTERN_OPEN_BRACES_RE = re.compile('(?P<start_brace>\{).*')
ROUTE_PATTERN_CLOSING_BRACES_RE = re.compile('\}.*')
QUOTES_RE = re.compile('(?P<quote_type>\'\'\'|"""|\'|").*') # order matters!


def search_quotes(line, escape_char='\\', quotes_re=QUOTES_RE):
    """
    This function is taken from Plim package: https://pypi.python.org/pypi/Plim/

    ``line`` may be empty

    :param line:
    :param escape_char:
    """
    match = quotes_re.match(line)
    if not match: return None

    find_seq = match.group('quote_type')
    find_seq_len = len(find_seq)
    pos = find_seq_len
    line_len = len(line)

    while pos < line_len:
        if line[pos] == escape_char:
            pos += 2
            continue
        if line[pos:].startswith(find_seq):
            return pos + find_seq_len
        pos += 1
    return None


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

        result = search_quotes(tail)
        if result is not None:
            buf.append(tail[:result])
            tail = tail[result:]
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
    if rules is None:
        rules = {}
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
                    # Use a simple greedy regular expression matching everything
                    rule = '.*'

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
    return reverse(route_name, args=elements, kwargs=kw)
