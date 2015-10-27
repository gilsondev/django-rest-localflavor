# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from rest_framework import serializers as drf_serializers

from rest_localflavor.test.testcases import DRFTestCase
from rest_localflavor.br import serializers


class BRStateFieldTest(TestCase):
    def setUp(self):
        self.valid_inputs = {
            "DF": "Distrito Federal",
            "GO": "Goiás"
        }

        self.invalid_inputs = {
            None: ["You can not insert a blank state."],
            "TX": ["You can not insert a invalid state."]
        }

    def test_required(self):
        field = serializers.BRStateField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation()
        self.assertEqual(exc_info.exception.detail,
                         self.invalid_inputs.get(None))

    def test_allow_blank(self):
        field = serializers.BRStateField(allow_blank=True)
        output = field.run_validation(None)
        self.assertIs(output, None)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_invalid_state(self):
        field = serializers.BRStateField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("TX")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid_inputs.get("TX"))


class BRCPFFieldTest(TestCase):
    def setUp(self):
        error_format = ['Invalid CPF number.']
        error_numbersonly = ['This field requires only numbers.']
        error_atmost = ['This field requires at most 11 digits or 14 characters.']
        self.valid = {
            '663.256.017-26': '663.256.017-26',
            '66325601726': '66325601726',
            '375.788.573-20': '375.788.573-20',
            '84828509895': '84828509895',
        }
        self.invalid = {
            None: error_format,
            '489.294.654-54': error_format,
            '375.788.573-XX': error_numbersonly,
            '375.788.573-000': error_atmost,
            '123.456.78': error_atmost,
            '123456789555': error_atmost,
        }

    def test_required(self):
        field = serializers.BRCPFField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation()
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get(None))

    def test_allow_blank(self):
        field = serializers.BRCPFField(allow_blank=True)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_invalid_format_cpf(self):
        field = serializers.BRCPFField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("489.294.654-54")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("489.294.654-54"))

    def test_invalid_numbers_cpf(self):
        field = serializers.BRCPFField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("375.788.573-XX")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("375.788.573-XX"))

    def test_invalid_atmost_chars_cpf(self):
        field = serializers.BRCPFField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("375.788.573-000")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("375.788.573-000"))

    def test_invalid_atleast_chars_cpf(self):
        field = serializers.BRCPFField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("123.456.78")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("123.456.78"))

    def test_valid_cpf(self):
        field = serializers.BRCPFField()
        output = field.run_validation("663.256.017-26")
        self.assertEqual(output, self.valid.get("663.256.017-26"))


class BRCNPJFieldTest(TestCase):
    def setUp(self):
        error_invalid = ['Invalid CNPJ number.']
        error_numbersonly = ['This field requires only numbers.']

        self.valid = {
            '64.132.916/0001-88': '64.132.916/0001-88',
            '64-132-916/0001-88': '64-132-916/0001-88',
            '64132916/0001-88': '64132916/0001-88',
        }

        self.invalid = {
            None: error_invalid,
            '12-345-678/9012-10': error_invalid,
            '12.345.678/9012-10': error_invalid,
            '12345678/9012-10': error_invalid,
            '64.132.916/0001-XX': error_numbersonly,
        }

    def test_required(self):
        field = serializers.BRCNPJField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation()
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get(None))

    def test_allow_blank(self):
        field = serializers.BRCNPJField(allow_blank=True)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_invalid_format_cnpj(self):
        field = serializers.BRCNPJField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("12-345-678/9012-10")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("12-345-678/9012-10"))

    def test_invalid_numbers_cnpj(self):
        field = serializers.BRCNPJField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("64.132.916/0001-XX")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("64.132.916/0001-XX"))


class BRZipCodeFieldTest(TestCase):
    def setUp(self):
        self.error_invalid = ['Enter a zip code in the format XXXXX-XXX, XX.XXX-XXX or XXXXXXXX.']

        self.valid = {
            '73.360-610': '73.360-610'
        }

        self.invalid = {
            None: self.error_invalid,
            '70.000-0000': self.error_invalid,
            '700000-000': self.error_invalid,
        }

    def test_required(self):
        field = serializers.BRZipCodeField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation()
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get(None))

    def test_allow_blank(self):
        field = serializers.BRZipCodeField(allow_blank=True)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_invalid_format_zipcode(self):
        field = serializers.BRZipCodeField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("70.000-0000")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("70.000-0000"))


        field = serializers.BRZipCodeField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation("700000-000")
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get("700000-000"))


class BRPhoneNumberFieldTest(DRFTestCase):
    def setUp(self):
        error_invalid = ['Phone numbers must be in either of the following formats: XX-XXXX-XXXX or XX-XXXXX-XXXX.']

        self.valid = {
            '41-3562-3464': '41-3562-3464',
            '4135623464': '41-3562-3464',
            '41 3562-3464': '41-3562-3464',
            '41 3562 3464': '41-3562-3464',
            '(41) 3562 3464': '41-3562-3464',
            '41.3562.3464': '41-3562-3464',
            '41.93562.3464': '41-93562-3464',
            '41.3562-3464': '41-3562-3464',
            ' (41) 3562.3464': '41-3562-3464',
            ' (41) 98765.3464': '41-98765-3464',
            '(16) 91342-4325': '16-91342-4325',
        }

        self.invalid = {
            None: error_invalid,
            '11-914-925': error_invalid,
            '11-9144-43925': error_invalid,
            '11-91342-94325': error_invalid,
            '411-9134-9435': error_invalid,
            '+55-41-3562-3464': error_invalid,
            '41 3562–3464': error_invalid,
        }

    def test_required(self):
        field = serializers.BRPhoneNumberField()
        with self.assertRaises(drf_serializers.ValidationError) as exc_info:
            field.run_validation()
        self.assertEqual(exc_info.exception.detail,
                         self.invalid.get(None))

    def test_allow_blank(self):
        field = serializers.BRPhoneNumberField(allow_blank=True)

        output = field.run_validation("")
        self.assertEqual(output, "")

    def test_valid(self):
        self.assertFieldOutput(serializers.BRPhoneNumberField, self.valid, self.invalid)
