import unittest

from category.domain.validators import CategoryRules, CategoryValidator, CategoryValidatorFactory

class TestCategoryValidatorUnit(unittest.TestCase):
    validator: CategoryValidator
    
    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()
        return super().setUp()
    
    def test_invalidation_cases_for_name_field(self):
        is_valid = self.validator.validate(None)
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field is required.'])
        
        is_valid = self.validator.validate({})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field is required.'])
        
        is_valid = self.validator.validate({'name': ''})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field may not be blank.'])
        
        is_valid = self.validator.validate({'name': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['This field may not be null.'])
        
        is_valid = self.validator.validate({'name': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['Not a valid string.'])
        
        is_valid = self.validator.validate({'name': 'a'*256})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], ['Ensure this field has no more than 255 characters.'])