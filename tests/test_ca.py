# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_localflavor.test.testcases import DRFTestCase
from rest_framework.exceptions import ValidationError

from rest_localflavor.ca import serializers


class FieldtestMixin(object):
    field_class = None
    valid = None
    invalid = None

    def test_required(self):
        field = self.field_class()
        with self.assertRaises(ValidationError) as exc_info:
            field.run_validation()
            self.assertEqual(exc_info.exception.detail, self.invalid.get(None))

    def test_allow_blank(self):
        field = self.field_class(allow_blank=True)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_valid(self):
        self.assertFieldOutput(self.field_class, self.valid, self.invalid)


class CAPostalCodeFieldTest(DRFTestCase, FieldtestMixin):
    def setUp(self):
        self.field_class = serializers.CAPostalCodeField

        error_invalid = ["Enter a postal code in the format XXX XXX."]

        self.valid = {
            'J0X 1G0': 'J0X 1G0',
            'K1N 5J9': 'K1N 5J9',
            'K7S 1W2': 'K7S 1W2',
            'K7S 3G5': 'K7S 3G5',
            'K7S 2B4': 'K7S 2B4',
            'K7S 1V7': 'K7S 1V7',
            'K7S 3V2': 'K7S 3V2',
        }

        self.invalid = {
            None: error_invalid,
            '': error_invalid,
            'a': error_invalid,
            'DDD 111': error_invalid,
            'FFF 222': error_invalid,
        }


class CAPhoneNumberFieldTest(DRFTestCase, FieldtestMixin):
    def setUp(self):
        self.field_class = serializers.CAPhoneNumberField

        error_invalid = ["Phone numbers must be in XXX-XXX-XXXX format."]

        self.valid = {
            '123-123-1234': '123-123-1234',
            '123 123-1234': '123-123-1234',
            '123 123 1234': '123-123-1234',
            ' 123 123 1234 ': '123-123-1234',
            '(123) 123 1234': '123-123-1234',
            ' (123) 123 1234 ': '123-123-1234',
            ' (123)-123-1234 ': '123-123-1234',
        }

        self.invalid = {
            None: error_invalid,
            '': error_invalid,
            'a': error_invalid,
            '+1 123-123-1234': error_invalid,
            '+1 123 123 1234': error_invalid,
            '+1 (123)-123-1234': error_invalid,
        }


class CAProvinceFieldTest(DRFTestCase, FieldtestMixin):
    def setUp(self):
        self.field_class = serializers.CAProvinceField

        error_invalid = ["Enter a Canadian province or territory."]

        self.valid = {
            'PE': 'PE',
            'pe': 'PE',
            'pei': 'PE',
            'p.e.i.': 'PE',
        }

        self.invalid = {
            None: error_invalid,
            '': error_invalid,
            'a': error_invalid,
            'XX': error_invalid,
            'AZ': error_invalid,
        }


class CASocialInsuranceNumberFieldTest(DRFTestCase, FieldtestMixin):
    def setUp(self):
        self.field_class = serializers.CASocialInsuranceNumberField

        error_invalid = ["Enter a valid Canadian Social Insurance number in XXX-XXX-XXX format."]

        self.valid = {
            '046-454-286': '046-454-286',
        }

        self.invalid = {
            None: error_invalid,
            '': error_invalid,
            'a': error_invalid,
            'abc-def-ghi': error_invalid,
            '111-222-333': error_invalid,
            'xxx/yyy/zzz': error_invalid,
            '046 454 286': error_invalid,
        }
