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
        faker.with_unique_entity_id(unique_entity_id)
        
        self.assertEqual(faker.unique_entity_id, unique_entity_id)
        
    def test_name_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.name, str)
        
        faker.with_name('name test')
        self.assertEqual(faker.name, 'name test')
    
    def test_description_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.description, str)
        
        faker.with_name('description test')
        self.assertEqual(faker.description, 'description test')
        
    def test_is_active_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertTrue(faker.is_active)
        
        faker.deactivate()
        self.assertFalse(faker.is_active)
        
        faker.activate()
        self.assertTrue(faker.is_active)
    
    def test_created_at_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_exception:
            faker = CategoryFakerBuilder.a_category()
            faker.created_at
        self.assertEqual(assert_exception.exception.args[0], 'Prop created_at does not have a factory, use "with methods"')
        
    def test_created_at_prop(self):
        created_at = datetime.now()
        
        faker = CategoryFakerBuilder.a_category()
        faker.with_created_at(created_at)
        
        self.assertEqual(faker.created_at, created_at)
    
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