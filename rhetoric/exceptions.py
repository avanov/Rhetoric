"""This module contains exception classes from Pyramid Web Framework."""

class ConfigurationError(Exception):
    """ Raised when inappropriate input values are supplied to an API
    method of a :term:`Configurator`"""


class CyclicDependencyError(Exception):
    """ This class is a copy of ``pyramid.exceptions.CyclicDependencyError``.

    The exception raised when the Pyramid topological sorter detects a
    cyclic dependency."""
    def __init__(self, cycles):
        self.cycles = cycles

    def __str__(self):
        L = []
        cycles = self.cycles
        for cycle in cycles:
            dependent = cycle
            dependees = cycles[cycle]
            L.append('%r sorts before %r' % (dependent, dependees))
        msg = 'Implicit ordering cycle:' + '; '.join(L)
        return msg
