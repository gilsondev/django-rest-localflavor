
from django.test import TestCase

from rest_localflavor.generic.checksums import luhn


class LuhnChecksumTestCase(TestCase):
    def setUp(self):
        self.valid_values = [
            79927398713,
            '79927398713',
        ]
        self.invalid_values = [
            72723846,
            'abc',
            {'a': 'b'},
            [1, 2, 3],
        ]

    def test_valid_values(self):
        for value in self.valid_values:
            self.assertEqual(luhn(value), True)

    def test_invalid_values(self):
        for value in self.invalid_values:
            self.assertEqual(luhn(value), False)
