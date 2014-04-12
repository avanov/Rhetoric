""" ADT stands for Algebraic data type
"""
from rhetoric.exceptions import ConfigurationError


class ADTConfiguratorMixin(object):

    def update_adt_registry(self, adt_meta):
        """

        :type adt_meta: dict
        """
        adt_type = adt_meta['type']
        self.adt[adt_type] = adt_meta

    def check_adt_consistency(self):
        for obj_id, adt_meta in self.adt.items():
            for case_name, case_meta in adt_meta['cases'].items():
                for variant, implementation in case_meta.items():
                    if implementation is None:
                        raise ConfigurationError(
                            'Case {case_name} of {type} is not exhaustive. '
                            'Here is the variant that is not matched: {variant} '
                            .format(
                                case_name=case_name,
                                type=str(adt_meta['type']),
                                variant=variant
                            )
                        )
        # All good. We no longer need the adt meta.
        delattr(self, 'adt')
