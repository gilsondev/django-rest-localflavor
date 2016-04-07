# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import django

from django.utils import six
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers as drf_serializers
from rest_framework.fields import empty

# MinValueValidator, MaxValueValidator et al. only accept `message` in 1.8+
if django.VERSION >= (1, 8):
    from django.core.validators import MinLengthValidator, MaxLengthValidator
else:
    from rest_framework.compat import MaxLengthValidator, MinLengthValidator

from .br_states import STATE_CHOICES

try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


class BRStateField(drf_serializers.ChoiceField):
    """
    A field for list brazilian states.
    """
    type_name = "BRStateField"

    default_error_messages = {
        'empty': _("You can not insert a blank state."),
        'invalid_choice': _("You can not insert a invalid state.")
    }
    initial = ''

    def __init__(self, choices=STATE_CHOICES, **kwargs):
        self.allow_blank = kwargs.get('allow_blank', False)
        super(BRStateField, self).__init__(choices, **kwargs)

    def run_validation(self, data=empty):
        if data in EMPTY_VALUES or not isinstance(data, six.text_type):
            if not self.allow_blank:
                self.fail('empty')
            return data
        return super(BRStateField, self).run_validation(data)

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        try:
            return self.choice_strings_to_values[six.text_type(data)]
        except KeyError:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        return super(BRStateField, self).to_representation(value)


class BRCPFField(drf_serializers.CharField):
    """
    This field validate a CPF number or a CPF string. A CPF number is
    compounded by XXX.XXX.XXX-VD. The two last digits are check digits.
    More information:
    http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
    """

    default_error_messages = {
        'invalid': _("Invalid CPF number."),
        'max_digits': _("""This field requires at most 11 digits or 14 characters."""),
        'digits_only': _("This field requires only numbers."),
        'max_length': _('Ensure this field has no more than {max_length} characters.'),
        'min_length': _('Ensure this field has at least {min_length} characters.')
    }

    def __init__(self, max_length=14, min_length=11, **kwargs):
        self.allow_blank = kwargs.get('allow_blank', False)
        self.max_length = kwargs.get('max_length', None)
        self.min_length = kwargs.get('min_length', None)
        super(BRCPFField, self).__init__(**kwargs)
        if self.max_length is not None:
            message = self.error_messages['max_length'].format(
                max_length=self.max_length)
            self.validators.append(
                MaxLengthValidator(self.max_length, message=message)
            )

        if self.min_length is not None:
            message = self.error_messages['min_length'].format(
                min_length=self.min_length)
            self.validators.append(
                MinLengthValidator(self.min_length, message=message)
            )

    def run_validation(self, value=empty):
        if value in EMPTY_VALUES or not isinstance(value, six.text_type):
            if not self.allow_blank:
                self.fail('invalid')
            return ''

        orig_value = value[:]
        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        try:
            int(value)
        except ValueError:
            self.fail('digits_only')
        if len(value) != 11:
            self.fail('max_digits')
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(
            range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(
            range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            self.fail('invalid')
        return orig_value


class BRCNPJField(drf_serializers.CharField):
    """
    This field validate a CNPJ number or a CNPJ string. A CNPJ number is
    compounded by XXX.XXX.XXX-VD. The two last digits are check digits.
    More information:
    https://pt.wikipedia.org/wiki/Cadastro_Nacional_da_Pessoa_Jur%C3%ADdica
    """

    default_error_messages = {
        'invalid': _("Invalid CNPJ number."),
        'digits_only': _("This field requires only numbers."),
        'max_digits': _("This field requires at least 14 digits"),
    }

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.get('allow_blank', False)
        super(BRCNPJField, self).__init__(**kwargs)

    def run_validation(self, value=empty):
        if value in EMPTY_VALUES or not isinstance(value, six.text_type):
            if not self.allow_blank:
                self.fail('invalid')
            return ''

        orig_value = value[:]
        if not value.isdigit():
            value = re.sub("[-/\.]", "", value)
        try:
            int(value)
        except ValueError:
            self.fail('digits_only')
        if len(value) != 14:
            self.fail('max_digits')
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(
            list(range(5, 1, -1)) + list(range(9, 1, -1)))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(
            list(range(6, 1, -1)) + list(range(9, 1, -1)))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            self.fail('invalid')

        return orig_value


class BRZipCodeField(drf_serializers.RegexField):
    """
    This field validate a Zip code number or a Zip code string. A Zip code is
    a number to represent a place, that compounded by XXXXX-XXX, XX.XXX-XXX or
    number only of 8 digits.
    More information:
    https://pt.wikipedia.org/wiki/C%C3%B3digo_de_Endere%C3%A7amento_Postal
    """
    default_error_messages = {
        'invalid': _('Enter a zip code in the format XXXXX-XXX, XX.XXX-XXX or XXXXXXXX.'),
    }

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.get('allow_blank', False)
        super(BRZipCodeField, self).__init__(
            r'^(\d{2}\.\d{3}|\d{5})(-\d{3}|\d{3})$', **kwargs
        )

    def run_validation(self, value=empty):
        if value in EMPTY_VALUES or not isinstance(value, six.text_type):
            if not self.allow_blank:
                self.fail('invalid')
            return ''
        return super(BRZipCodeField, self).run_validation(value)


class BRPhoneNumberField(drf_serializers.CharField):
    """
    A form field that validates input as a Brazilian phone number, that must
    be in either of the following formats: XX-XXXX-XXXX or XX-XXXXX-XXXX.
    """
    default_error_messages = {
        'required': _(('Phone numbers must be in either of the following '
                      'formats: XX-XXXX-XXXX or XX-XXXXX-XXXX.')),
        'invalid': _(('Phone numbers must be in either of the following '
                      'formats: XX-XXXX-XXXX or XX-XXXXX-XXXX.')),
    }

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.get('allow_blank', False)
        super(BRPhoneNumberField, self).__init__(**kwargs)

    def run_validation(self, value=empty):
        if value in EMPTY_VALUES or not isinstance(value, six.text_type):
            if not self.allow_blank:
                self.fail('invalid')
            else:
                return value

        phone_digits_re = re.compile(r'^(\(\d{2}\)|\d{2})[-\.\s]?(\d{4,5})[-\.\s]?(\d{4})$')
        value = re.sub('(\(|\)|\s+)', '', smart_text(value))
        m = phone_digits_re.search(value)
        if m:
            return '%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
        else:
            self.fail('invalid')
