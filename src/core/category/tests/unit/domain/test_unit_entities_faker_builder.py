from datetime import datetime
import unittest
from core.__seedwork.domain.value_objects import UniqueEntityId
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
    
    def test_build(self):
        # tmp = CategoryFakerBuilder.a_category()
        # print(CategoryFakerBuilder.a_category().build())
        # print(CategoryFakerBuilder.the_categories(2).build())
        
        faker = CategoryFakerBuilder.the_categories(2)
        uuid = UniqueEntityId()
        date = datetime.now()
        faker = faker.with_name(lambda index: 'Moaaaaaaaaa' + str(index))
        faker = faker.with_unique_entity_id(uuid).with_created_at(date)
        print(faker.build())
        # print(faker.name)
        # print(faker.name)
        # print(faker.name)
        # print(faker.name)