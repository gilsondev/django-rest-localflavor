
import re

from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import empty

from ..generic.checksums import luhn


sin_re = re.compile(r"^(\d{3})-(\d{3})-(\d{3})$")


class CASocialInsuranceNumberField(serializers.CharField):
    """
    A Canadian Social Insurance Number (SIN).

    Checks the following rules to determine whether the number is valid:

    * Conforms to the XXX-XXX-XXX format.

    * Passes the check digit process "Luhn Algorithm"
         See: http://en.wikipedia.org/wiki/Social_Insurance_Number
    """

    default_error_messages = {
        'invalid': _('Enter a valid Canadian Social Insurance number in XXX-XXX-XXX format.'),
    }

    def __init__(self, *args, **kwargs):
        super(CASocialInsuranceNumberField, self).__init__(*args, **kwargs)
        self.error_messages['blank'] = self.error_messages['invalid']
        self.error_messages['null'] = self.error_messages['invalid']

    def run_validation(self, value=empty):
        super(CASocialInsuranceNumberField, self).run_validation(value)
        if value in EMPTY_VALUES:
            return ''

        match = re.match(sin_re, value)
        if not match:
            self.fail('invalid')

        number = '%s-%s-%s' % (match.group(1), match.group(2), match.group(3))
        check_number = '%s%s%s' % (
            match.group(1),
            match.group(2),
            match.group(3))
        if not luhn(check_number):
            self.fail('invalid')
        return number
