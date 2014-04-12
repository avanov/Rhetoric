import re
import venusian


ADT_VARIANT_NAME_RE = re.compile('[A-Z][0-9A-Z_]*')


class ADTMeta(type):
    def __new__(mcs, class_name, bases, attrs):
        cls = type.__new__(mcs, class_name, bases, attrs)
        variants = set([name for name in attrs if ADT_VARIANT_NAME_RE.match(name)])
        values = {attrs[var_name]: var_name for var_name in variants}
        setattr(cls, '__adt__', {
            'type': str(cls),
            # set of adt variants
            'variants': variants,
            # dict of value => variant mappings
            'values': values,
            'cases': {},
            # dict of value => ADTMatch instances.
            # Used by .match() for O(1) result retrieval
            'matches': {}
        })
        return cls


class adt(object):
    __metaclass__ = ADTMeta
    venusian = venusian

    class Mismatch(Exception):
        pass

    @classmethod
    def values(cls):
        return set(cls.__adt__['values'].keys())

    @classmethod
    def match(cls, value):
        """
        :rtype: :class:`rhetoric.adt.ADTMatch`
        """
        try:
            variant = cls.__adt__['values'][value]
        except KeyError:
            raise cls.Mismatch(
                u'Variant value "{value}" is not a part of the type {type}: {values}'.format(
                    value=value,
                    type=cls.__adt__['type'],
                    values=u', '.join(['{val} => {var}'.format(val=val, var=var)
                                       for val, var in cls.__adt__['values'].items()])
                )
            )

        return cls.__adt__['matches'][variant]


    def __init__(self, variant, case):
        """
        :type variant: str
        :type case: str
        """
        cases_dict = self.__adt__['cases']
        variants = self.__adt__['variants']

        if variant not in variants:
            raise TypeError(
                'Variant {variant} does not belong to the type {type}'.format(
                    variant=variant,
                    type=self.__adt__['type']
                )
            )
        cases_dict.setdefault(case, {v: None for v in variants})
        self.variant = variant
        self.case = case

    def __call__(self, wrapped):

        def callback(scanner, name, obj):
            cases_dict = self.__adt__['cases']
            case_implementations = cases_dict[self.case]
            if case_implementations[self.variant] is not None:
                raise TypeError(
                    'Variant {variant} of {type} is already bound to the case {case}: {impl}'.format(
                        variant=self.variant,
                        type=self.__adt__['type'],
                        case=self.case,
                        impl=str(obj)
                    )
                )
            case_implementations[self.variant] = obj
            # Re-calculate matches
            self.__adt__['matches'] = {
                variant: ADTMatch({case: impl[variant] for case, impl in cases_dict.items()})
                for variant in self.__adt__['variants']
            }
            scanner.config.update_adt_registry(self.__adt__)

        info = self.venusian.attach(wrapped, callback, category='rhetoric')
        return wrapped


class ADTMatch(object):
    def __init__(self, attrs):
        """
        :type attrs: dict
        """
        self.__dict__.update(attrs)
