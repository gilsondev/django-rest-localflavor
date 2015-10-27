# -*- coding: utf-8 -*-

from django.test import SimpleTestCase
# from django.utils.encoding import force_text
# from django.core.validators import EMPTY_VALUES

from rest_framework.serializers import ValidationError
from rest_framework.serializers import CharField


class DRFTestCase(SimpleTestCase):
    """
    Test case created to overrited the assertFieldOutput, to
        verify if test with valid and invalid data it was a success.
    """

    def assertFieldOutput(self, fieldclass, valid, invalid, field_args=None,
                          field_kwargs=None, empty_value=''):
        """
        Asserts that a form field behaves correctly with various inputs.
        Args:
            fieldclass: the class of the field to be tested.
            valid: a dictionary mapping valid inputs to their expected
                    clean values.
            invalid: a dictionary mapping invalid inputs to one or more
                    raised error messages.
            field_args: the args passed to instantiate the field
            field_kwargs: the kwargs passed to instantiate the field
            empty_value: the expected run_validation output for inputs in empty_values
        """
        if field_args is None:
            field_args = []
        if field_kwargs is None:
            field_kwargs = {}
        required = fieldclass(*field_args, **field_kwargs)
        optional = fieldclass(*field_args,
                              **dict(field_kwargs, required=False, allow_blank=True))
        # test valid inputs
        for input, output in valid.items():
            self.assertEqual(required.run_validation(input), output)
            self.assertEqual(optional.run_validation(input), output)
        # test invalid inputs
        for input, errors in invalid.items():
            with self.assertRaises(ValidationError) as context_manager:
                required.run_validation(input)
            self.assertEqual(context_manager.exception.detail, errors)

        # TODO: Fix optional to serializer fields
        #     with self.assertRaises(ValidationError) as context_manager:
        #         optional.run_validation(input)

        #     self.assertEqual(context_manager.exception.detail, errors)
        # test required inputs
        # error_required = [force_text(required.error_messages['required'])]
        # for e in EMPTY_VALUES:
        #     with self.assertRaises(ValidationError) as context_manager:
        #         required.run_validation(e)
        #     self.assertEqual(context_manager.exception.detail,
        #                      error_required)
        #     self.assertEqual(optional.run_validation(e), empty_value)
        # test that max_length and min_length are always accepted
        if issubclass(fieldclass, CharField):
            field_kwargs.update({'min_length': 2, 'max_length': 20})
            self.assertIsInstance(fieldclass(*field_args, **field_kwargs),
                                  fieldclass)
