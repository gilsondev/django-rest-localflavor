
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as __

from rest_framework import serializers
from rest_framework.fields import empty


class USStateField(serializers.CharField):
    """
    A field that validates its input is a U.S. state name or abbreviation.
    It normalizes the input to the standard two-letter postal service
    abbreviation for the given province.
    """

    default_error_messages = {
        'invalid': __('Enter a U.S. state or territory.'),
    }

    def __init__(self, *args, **kwargs):
        super(USStateField, self).__init__(*args, **kwargs)
        self.error_messages['blank'] = self.error_messages['invalid']
        self.error_messages['null'] = self.error_messages['invalid']

    def run_validation(self, data=empty):
        super(USStateField, self).run_validation(data)
        if data in EMPTY_VALUES:
            return ''

        try:
            value = data.strip().lower()
        except AttributeError:
            pass
        else:
            # Load data in memory only when it is required, see also #17275
            from .us_states import STATES_NORMALIZED
            try:
                return STATES_NORMALIZED[value.strip().lower()]
            except KeyError:
                pass
        self.fail('invalid')
