from datetime import datetime
import unittest
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.domain.entities_faker_builder import CategoryFakerBuilder


class TestEntitiesFakerBuilder(unittest.TestCase):
    
    def test_unique_entity_id_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_exception:
            faker = CategoryFakerBuilder.a_category()
            faker.unique_entity_id
        self.assertEqual(assert_exception.exception.args[0], 'Prop unique_entity_id does not have a factory, use "with methods"')
    
    def test_unique_entity_id_prop(self):
        unique_entity_id = UniqueEntityId()
        
        faker = CategoryFakerBuilder.a_category()
        this = faker.with_unique_entity_id(unique_entity_id)
        
        self.assertEqual(faker.unique_entity_id, unique_entity_id)
        self.assertIsInstance(this, CategoryFakerBuilder)
        
    def test_name_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.name, str)
        
        this = faker.with_name('name test')
        self.assertEqual(faker.name, 'name test')
        self.assertIsInstance(this, CategoryFakerBuilder)
        
    def test_invalid_cases_for_name_prop(self):
        faker = CategoryFakerBuilder.a_category()
        
        name_value = faker.with_invalid_name_none().name
        self.assertIsNone(name_value)
        
        name_value = faker.with_invalid_name_empty().name
        self.assertEqual(name_value, '')
        
        name_value = faker.with_invalid_name_not_string().name
        self.assertEqual(name_value, 123)
        
        name_value = faker.with_invalid_name_not_string(10).name
        self.assertEqual(name_value, 10)
        
        name_value = faker.with_invalid_name_too_long().name
        self.assertEqual(len(name_value), 256)
        
    def test_invalid_cases_for_description_prop(self):
        faker = CategoryFakerBuilder.a_category()
        
        this = faker.with_invalid_description_not_string()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(this.description, 123)
        
    def test_invalid_cases_for_is_active(self):
        faker = CategoryFakerBuilder.a_category()
        
        this = faker.with_invalid_is_active_none()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertIsNone(this.is_active)
        
        this = faker.with_invalid_is_active_empty()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(this.is_active, '')
        
        this = faker.with_invalid_is_active_not_boolean()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(this.is_active, 123)
    
    def test_description_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.description, str)
        
        this = faker.with_description('description test')
        self.assertEqual(faker.description, 'description test')
        self.assertIsInstance(this, CategoryFakerBuilder)
        
    def test_is_active_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertTrue(faker.is_active)
        
        this = faker.deactivate()
        self.assertFalse(faker.is_active)
        self.assertIsInstance(this, CategoryFakerBuilder)
        
        this = faker.activate()
        self.assertTrue(faker.is_active)
        self.assertIsInstance(this, CategoryFakerBuilder)
    
    def test_created_at_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_exception:
            faker = CategoryFakerBuilder.a_category()
            faker.created_at
        self.assertEqual(assert_exception.exception.args[0], 'Prop created_at does not have a factory, use "with methods"')
        
    def test_created_at_prop(self):
        created_at = datetime.now()
        
        faker = CategoryFakerBuilder.a_category()
        this = faker.with_created_at(created_at)
        
        self.assertEqual(faker.created_at, created_at)
        self.assertIsInstance(this, CategoryFakerBuilder)
    
    def test_build_a_category(self):
        faker = CategoryFakerBuilder.a_category()
        category = faker.build()
        
        self.assert_category_props_types(category)
        
        unique_entity_id = UniqueEntityId()
        created_at = datetime.now()
        
        builder = faker.with_unique_entity_id(unique_entity_id)\
            .with_name('name test')\
            .with_description('description test')\
            .deactivate()\
            .with_created_at(created_at)
        
        category = builder.build()
        self.assert_category(category, unique_entity_id, created_at)
        
        builder= builder.activate()
        category = builder.build()
        self.assertTrue(category.is_active)
        
    def test_build_the_categories(self):
        faker = CategoryFakerBuilder.the_categories(2)
        categories = faker.build()
        
        self.assertIsNotNone(categories)
        self.assertIsInstance(categories, list)
        self.assertEqual(len(categories), 2)
        
        for category in categories:
            self.assert_category_props_types(category)
        
        unique_entity_id = UniqueEntityId()
        created_at = datetime.now()
        
        builder = faker.with_unique_entity_id(unique_entity_id)\
            .with_name('name test')\
            .with_description('description test')\
            .deactivate()\
            .with_created_at(created_at)
        
        categories = builder.build()
        for category in categories:
            self.assert_category(category, unique_entity_id, created_at)
        
        builder= builder.activate()
        categories = builder.build()
        for category in categories:
            self.assertTrue(category.is_active)
            
    def assert_category_props_types(self, category: Category):
        self.assertIsInstance(category.unique_entity_id, UniqueEntityId)
        self.assertIsInstance(category.name, str)
        self.assertIsInstance(category.description, str)
        self.assertIsInstance(category.is_active, bool)
        self.assertIsInstance(category.created_at, datetime)
        self.assertTrue(category.is_active)
        
    def assert_category(self, category: Category, unique_entity_id: UniqueEntityId, created_at: datetime):
        self.assertEqual(category.unique_entity_id, unique_entity_id)
        self.assertEqual(category.name, 'name test')
        self.assertEqual(category.description, 'description test')
        self.assertFalse(category.is_active)
        self.assertEqual(category.created_at, created_at)