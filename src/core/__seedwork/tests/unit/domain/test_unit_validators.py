import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from dataclasses import fields
from rest_framework.serializers import Serializer

from __seedwork.domain.validators import (
    ValidatorRules,
    ValidationException,
    ValidatorFieldsInterface,
    DRFValidator
)


class TestValidatorRulesUnit(unittest.TestCase):
    def test_values_method(self):
        validator = ValidatorRules.values('some value', 'some prop')

        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'some value')
        self.assertEqual(validator.prop, 'some prop')

    def test_required_rule(self):
        invalid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop'}
        ]

        for item in invalid_data:
            msg = f'value: {item["value"]}, prop: {item["prop"]}'
            with self.assertRaises(ValidationException,
                                   msg=msg) as assert_error:
                ValidatorRules(item['value'], item['prop']).required()

            self.assertEqual('The prop is required',
                             assert_error.exception.args[0],)

        valid_data = [
            {'value': 'test', 'prop': 'prop'},
            {'value': 5, 'prop': 'prop'},
            {'value': 0, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
        ]

        for item in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                item['value'], item['prop']).required(), ValidatorRules)

    def test_string_rule(self):
        invalid_data = [
            {'value': 5, 'prop': 'prop'},
            {'value': True, 'prop': 'prop'},
            {'value': {}, 'prop': 'prop'},
        ]

        for item in invalid_data:
            msg = f'value: {item["value"]}, prop: {item["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules(item['value'], item['prop']).string()

            self.assertEqual(
                'The prop must be a string',
                assert_error.exception.args[0],
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop'},
            {'value': 'some value', 'prop': 'prop'},
        ]

        for item in valid_data:
            self.assertIsInstance(ValidatorRules(
                item['value'], item['prop']).string(), ValidatorRules)

    def test_max_rule(self):
        invalid_data = [
            {'value': "t" * 5, 'prop': 'prop'}
        ]

        for item in invalid_data:
            msg = f'value: {item["value"]}, prop: {item["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules(item['value'], item['prop']).max_length(4)

            self.assertEqual(
                'The prop must be less than 4 characters',
                assert_error.exception.args[0],
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "t" * 5, 'prop': 'prop'},
        ]

        for item in valid_data:
            self.assertIsInstance(
                ValidatorRules(item['value'], item['prop']).max_length(5),
                ValidatorRules,
            )

    def test_boolean_rule(self):
        invalid_data = [
            {'value': "", 'prop': 'prop'},
            {'value': 5, 'prop': 'prop'},
            {'value': {}, 'prop': 'prop'},
        ]

        for item in invalid_data:
            msg = f'value: {item["value"]}, prop: {item["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules(item['value'], item['prop']).boolean()

            self.assertEqual(
                'The prop must be a boolean',
                assert_error.exception.args[0]
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': True, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
        ]

        for item in valid_data:
            self.assertIsInstance(
                ValidatorRules(item['value'], item['prop']).boolean(),
                ValidatorRules
            )

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None, 'prop').required().string().max_length(5)

        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(3, 'prop').required().string().max_length(5)

        self.assertEqual(
            'The prop must be a string',
            assert_error.exception.args[0]
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                't' * 6, 'prop').required().string().max_length(5)

        self.assertEqual(
            'The prop must be less than 5 characters',
            assert_error.exception.args[0]
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(None, 'prop').required().boolean()

        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0]
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(5, 'prop').required().boolean()

        self.assertEqual(
            'The prop must be a boolean',
            assert_error.exception.args[0]
        )

    def test_valid_cases_for_combination_between_rules(self):
        ValidatorRules('test', 'prop').required().string()
        ValidatorRules('t' * 5, 'prop').required().string().max_length(5)

        ValidatorRules(True, 'prop').required().boolean()
        ValidatorRules(False, 'prop').required().boolean()


class TestValidatorFieldsInterfaceUnit(unittest.TestCase):
    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            ValidatorFieldsInterface()  # pylint: disable=abstract-class-instantiated
        self.assertEqual("Can't instantiate abstract class ValidatorFieldsInterface " +
                         "with abstract method validate",
                         assert_error.exception.args[0])

    def test_valid_fields(self):
        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_class[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)


class TestDRFValidatorUnit(unittest.TestCase):
    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(
        Serializer,
        'validated_data',
        return_value={'field': ['value']},
        new_callable=PropertyMock
    )
    def test_if_validated_data_is_set(self,
                                      mock_validated_data: PropertyMock,  # pylint: disable=unused-argument
                                      mock_is_valid: MagicMock):
        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {'field': ['value']})
        mock_is_valid.assert_called_once()

    @patch.object(Serializer, 'is_valid', return_value=False)
    @patch.object(
        Serializer,
        'errors',
        return_value={'field': ['some error']},
        new_callable=PropertyMock
    )
    def test_if_errors_is_set(self,
                              mock_errors: PropertyMock,  # pylint: disable=unused-argument
                              mock_is_valid: MagicMock):
        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        self.assertFalse(is_valid)
        self.assertEqual(validator.errors, {'field': ['some error']})
        mock_is_valid.assert_called_once()