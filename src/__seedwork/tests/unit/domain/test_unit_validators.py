import unittest

from __seedwork.domain.validators import ValidatorRules, ValidationException


class TestValidatorRules(unittest.TestCase):
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
                
            self.assertEquals(
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
