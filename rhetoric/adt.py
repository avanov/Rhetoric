import re
import venusian
import six


ADT_VARIANT_NAME_RE = re.compile('^[A-Z][0-9A-Z_]*$')


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

    def is_primitive_type(self):
        if isinstance(self.value, six.string_types):
            primitive_type = True
        elif isinstance(self.value, six.integer_types):
            primitive_type = True
        else:
            primitive_type = False
        return primitive_type


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
                    # venusian may scan the same declarations multiple times during the app initialization,
                    # therefore we allow re-assignment of the same case implementations and prohibit
                    # any new implementations
                    if case_implementations[self.name] is not obj:
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

        variants = {}
        for attr_name, value in attrs.items():
            if not ADT_VARIANT_NAME_RE.match(attr_name):
                continue
            variant = ADTVariant(variant_of=cls, name=attr_name, value=value)
            setattr(cls, attr_name, variant)
            variants[attr_name] = variant

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
            'matches': {
                variant: {} for variant in variants
            }
        }
        return cls


@six.add_metaclass(ADTMeta)
class adt(object):
    __adt__ = {}

    class Mismatch(Exception):
        pass

    class PatternError(Exception):
        pass

    @classmethod
    def values(cls):
        return set(cls.__adt__['values'].keys())

    @classmethod
    def match(cls, value):
        """
        :rtype: dict or :class:`types.FunctionType`
        """
        variant = None
        for variant_name, variant_type in cls.__adt__['variants'].items():
            if variant_type.is_primitive_type():
                # We compare primitive types with equality matching
                if value == variant_type.value:
                    variant = variant_name
                    break
            else:
                # We compare non-primitive types with type checking
                if isinstance(value, variant_type.value):
                    variant = variant_name
                    break

        if variant is None:
            raise cls.Mismatch(
                u'Variant value "{value}" is not a part of the type {type}: {values}'.format(
                    value=value,
                    type=cls.__adt__['type'],
                    values=u', '.join(['{val} => {var}'.format(val=val, var=var)
                                       for val, var in cls.__adt__['values'].items()])
                )
            )

        return cls.__adt__['matches'][variant]

    @classmethod
    def inline_match(cls, **inline_cases):
        all_cases = set(cls.__adt__['variants'].keys())
        inline_cases = inline_cases.items()
        checked_cases = []
        for variant_name, fun in inline_cases:
            try:
                variant = cls.__adt__['variants'][variant_name]
            except KeyError:
                raise cls.PatternError(
                    'Variant {variant} does not belong to the type {type}'.format(
                        variant=str(variant_name),
                        type=cls.__adt__['type'],
                    )
                )
            all_cases.remove(variant.name)
            checked_cases.append((variant, fun))

        if all_cases:
            raise cls.PatternError(
                'Inline cases are not exhaustive.\n'
                'Here is the variant that is not matched: {variant} '.format(
                    variant=list(all_cases)[0]
                )
            )

        def matcher(value):
            for variant, fun in checked_cases:
                if variant.is_primitive_type():
                    if value == variant.value:
                        return fun
                else:
                    if isinstance(value, variant.value):
                        return fun

            raise cls.Mismatch(
                u'Variant value "{value}" is not a part of the type {type}: {values}'.format(
                    value=value,
                    type=cls.__adt__['type'],
                    values=u', '.join(['{val} => {var}'.format(val=val, var=var)
                                       for val, var in cls.__adt__['values'].items()])
                )
            )
        return matcher

    def __init__(self):
        raise TypeError('adt is a type, not an instance.')
