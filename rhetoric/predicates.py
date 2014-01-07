import operator
from pkg_resources import parse_version


OPERATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '==': operator.eq,
    '>=': operator.ge,
    '<=': operator.le
}


def match_api_version(request_version, allowed_version):
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
        operation = OPERATORS.get(distinct_version[:2])
        if operation:
            # prepare cases #2, #5, #6
            compare_with = distinct_version[2:]
        else:
            operation = OPERATORS.get(distinct_version[0])
            if operation:
                # prepare cases #3, #4
                compare_with = distinct_version[1:]
            else:
                # prepare case #1
                compare_with = distinct_version
                operation = OPERATORS['==']

        # evaluate the case
        matched = operation(parse_version(request_version), parse_version(compare_with))
        if not matched:
            return False

    return True
