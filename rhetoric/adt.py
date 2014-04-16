import re
import venusian
import six


ADT_VARIANT_NAME_RE = re.compile('[A-Z][0-9A-Z_]*')


class ADTVariant(object):
    venusian = venusian

    def __init__(self, variant_of, name, value):
        """

        :param variant_of:
        :param name: variant name (uppercase variant name)
        :param value: variant value
        """
        self.variant_of = variant_of
        self.name = name
        self.value = value


    def __call__(self, case_name):
        """ This method is called when we declare variant cases. For instance:

            >>> class Language(adt):
            >>>     ENGLISH = 'en'
            >>>
            >>> @Language.ENGLISH('case_name')
            >>> def case_implementation():
            >>>     pass
            >>>

        :param case_name:
        :type case_name: str
        """
        cases_dict = self.variant_of.__adt__['cases']
        variants = self.variant_of.__adt__['variants']

        cases_dict.setdefault(case_name, {v: None for v in variants})

        def wrapper(wrapped):
            def callback(scanner, name, obj):
                """ This method will be called by venusian.
                The ``callback`` name is not reserved, we just pass this callable
                to ``self.venusian.attach()`` below. Although, callback's arguments list is strictly defined.
                """
                cases_dict = self.variant_of.__adt__['cases']
                case_implementations = cases_dict[case_name]
                if case_implementations[self.name] is not None:
                    raise TypeError(
                        'Variant {variant} of {type} is already bound to the case {case} => {impl}. '
                        'Conflict at {target}'.format(
                            variant=self.name,
                            type=self.variant_of.__adt__['type'],
                            case=case_name,
                            impl=str(case_implementations[self.name]),
                            target=str(obj)
                        )
                    )
                case_implementations[self.name] = obj
                # Re-calculate matches
                self.variant_of.__adt__['matches'] = {
                    variant: {case: impl[variant] for case, impl in cases_dict.items()}
                    for variant in self.variant_of.__adt__['variants']
                }
                scanner.config.update_adt_registry(self.variant_of.__adt__)

            info = self.venusian.attach(wrapped, callback, category='rhetoric')
            return wrapped
        return wrapper


class ADTMeta(type):
    def __new__(mcs, class_name, bases, attrs):
        cls = type.__new__(mcs, class_name, bases, attrs)

        variants = set()
        for attr_name, value in attrs.items():
            if not ADT_VARIANT_NAME_RE.match(attr_name):
                continue
            setattr(cls, attr_name, ADTVariant(variant_of=cls, name=attr_name, value=value))
            variants.add(attr_name)

        values = {attrs[variant_name]: variant_name for variant_name in variants}
        cls.__adt__ = {
            'type': str(cls),
            # set of adt variants
            'variants': variants,
            # dict of value => variant mappings
            'values': values,
            'cases': {},
            # dict of value => match instances.
            # Used by .match() for O(1) result retrieval
            'matches': {}
        }
        return cls


@six.add_metaclass(ADTMeta)
class adt(object):
    __adt__ = {}

    class Mismatch(Exception):
        pass

    @classmethod
    def values(cls):
        return set(cls.__adt__['values'].keys())

    @classmethod
    def match(cls, value):
        """
        :rtype: dict
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

    def __init__(self):
        raise TypeError('adt is a type, not an instance.')
