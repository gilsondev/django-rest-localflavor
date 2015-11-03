# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_localflavor.test.testcases import DRFTestCase
from rest_framework.exceptions import ValidationError

from rest_localflavor.ca import serializers


class CASocialInsuranceNumberFieldTest(DRFTestCase):
    def setUp(self):
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

    def test_required(self):
        field = serializers.CASocialInsuranceNumberField()
        with self.assertRaises(ValidationError) as exc_info:
            field.run_validation()
            self.assertEqual(exc_info.exception.detail, self.invalid.get(None))

    def test_allow_blank(self):
        field = serializers.CASocialInsuranceNumberField(allow_blank=True)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_valid(self):
        self.assertFieldOutput(serializers.CASocialInsuranceNumberField, self.valid, self.invalid)
