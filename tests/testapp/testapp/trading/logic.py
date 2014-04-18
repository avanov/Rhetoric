from .models import Instruction


__all__ = ['filter_by_oid']


def filter_by_oid(instructions, oid):
    """ For a given list of instructions and an Order ID,
    return the list of instructions that reference that Order ID.

    :param instructions: list of instructions
    :type instructions: list or tuple
    :param oid: Order ID
    :type oid: int
    :return: list of instructions that reference ``oid``
    :rtype: list
    """
    # In python3, filter, map, zip, etc return an object which is iterable, but not a list.
    return list(filter(
        lambda i: Instruction.match(i)['filter_by_oid'](i, oid),
        instructions))


@Instruction.ORDER('filter_by_oid')
def filter_order_by_oid(order, oid):
    """

    :param order:
    :type order: :class:`tests.testapp.testapp.trading.models.Order`
    :param oid: Order ID
    :type oid: int
    """
    return order.tid == oid


@Instruction.CANCEL('filter_by_oid')
def filter_cancel_by_oid(cancel, oid):
    """

    :param cancel:
    :type cancel: :class:`tests.testapp.testapp.trading.models.Cancel`
    :param oid: Order ID
    :type oid: int
    """
    return cancel.xtid == oid

@Instruction.CANCEL_REPLACE('filter_by_oid')
def filter_cancel_replace_by_oid(cr, oid):
    """

    :param cr:
    :type cr: :class:`tests.testapp.testapp.trading.models.CancelReplace`
    :param oid:
    :return:
    """
    return cr.xr_tid == oid


# Alternative way
# ---------------

inline_matcher = Instruction.inline_match(
    ORDER = lambda o, oid: o.tid == oid,
    CANCEL = lambda c, oid: c.xtid == oid,
    CANCEL_REPLACE = lambda cr, oid: cr.xr_tid == oid
)

def filter_by_oid_alt(instructions, oid):
    """ For a given list of instructions and an Order ID,
    return the list of instructions that reference that Order ID.

    :param instructions: list of instructions
    :type instructions: list or tuple
    :param oid: Order ID
    :type oid: int
    :return: list of instructions that reference ``oid``
    :rtype: list
    """
    # In python3, filter, map, zip, etc return an object which is iterable, but not a list.
    return list(filter(
        lambda i: inline_matcher(i)(i, oid),
        instructions))
