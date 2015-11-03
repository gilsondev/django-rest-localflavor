
import re

from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from rest_framework import serializers
from rest_framework.fields import empty

from ..generic.checksums import luhn


postcode_re = re.compile(r'^([ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]) *(\d[ABCEGHJKLMNPRSTVWXYZ]\d)$')
phone_digits_re = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')
sin_re = re.compile(r"^(\d{3})-(\d{3})-(\d{3})$")


class CAPostalCodeField(serializers.CharField):
    """
    Canadian postal code field.

    Validates against known invalid characters: D, F, I, O, Q, U
    Additionally the first character cannot be Z or W.
    For more info see:
    http://www.canadapost.ca/tools/pg/manual/PGaddress-e.asp#1402170
    """

    default_error_messages = {
        'invalid': _('Enter a postal code in the format XXX XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(CAPostalCodeField, self).__init__(*args, **kwargs)
        self.error_messages['blank'] = self.error_messages['invalid']
        self.error_messages['null'] = self.error_messages['invalid']

    def run_validation(self, data=empty):
        data = super(CAPostalCodeField, self).run_validation(data)
        if data in EMPTY_VALUES:
            return ''

        postcode = data.upper().strip()
        m = postcode_re.match(postcode)
        if not m:
            self.fail('invalid')
        return "%s %s" % (m.group(1), m.group(2))


class CAPhoneNumberField(serializers.CharField):
    """
    Canadian phone number field.
    """

    default_error_messages = {
        'invalid': _('Phone numbers must be in XXX-XXX-XXXX format.'),
    }

    def __init__(self, *args, **kwargs):
        super(CAPhoneNumberField, self).__init__(*args, **kwargs)
        self.error_messages['blank'] = self.error_messages['invalid']
        self.error_messages['null'] = self.error_messages['invalid']

    def run_validation(self, data=empty):
        super(CAPhoneNumberField, self).run_validation(data)
        if data in EMPTY_VALUES:
            return ''

        value = re.sub('(\(|\)|\s+)', '', smart_text(data))
        m = phone_digits_re.search(value)
        if m:
            return '%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
        self.fail('invalid')


class CAProvinceField(serializers.CharField):
    """
    A field that validates its input is a Canadian province name or abbreviation.
    It normalizes the input to the standard two-letter postal service
    abbreviation for the given province.
    """

    default_error_messages = {
        'invalid': _('Enter a Canadian province or territory.'),
    }

    def __init__(self, *args, **kwargs):
        super(CAProvinceField, self).__init__(*args, **kwargs)
        self.error_messages['blank'] = self.error_messages['invalid']
        self.error_messages['null'] = self.error_messages['invalid']

    def run_validation(self, data=empty):
        super(CAProvinceField, self).run_validation(data)
        if data in EMPTY_VALUES:
            return ''

        try:
            value = data.strip().lower()
        except AttributeError:
            pass
        else:
            # Load data in memory only when it is required, see also #17275
            from .ca_provinces import PROVINCES_NORMALIZED
            try:
                return PROVINCES_NORMALIZED[value.strip().lower()]
            except KeyError:
                pass
        self.fail('invalid')


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

    def run_validation(self, data=empty):
        super(CASocialInsuranceNumberField, self).run_validation(data)
        if data in EMPTY_VALUES:
            return ''

        match = re.match(sin_re, data)
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
