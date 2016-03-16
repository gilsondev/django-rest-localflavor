# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_localflavor.test.testcases import DRFTestCase
from rest_framework.exceptions import ValidationError

from rest_localflavor.us import serializers


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


class USStateFieldTest(DRFTestCase, FieldtestMixin):
    def setUp(self):
        self.field_class = serializers.USStateField

        error_invalid = ["Enter a U.S. state or territory."]

        self.valid = {
            'CA': 'CA',
            'ca': 'CA',
            'calf': 'CA',
            'calif': 'CA',
            'california': 'CA',
        }

        self.invalid = {
            None: error_invalid,
            '': error_invalid,
            'a': error_invalid,
            'XX': error_invalid,
            'AX': error_invalid,
        }
