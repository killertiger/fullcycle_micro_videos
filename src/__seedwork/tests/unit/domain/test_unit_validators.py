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
                             assert_error.exception.args[0])

        valid_data = [
            {'value': 'test', 'prop': 'prop'},
            {'value': 5, 'prop': 'prop'},
            {'value': 0, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
        ]

        for item in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                item['value'], item['prop']).required(), ValidatorRules)
