from datetime import datetime
import unittest
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities_faker_builder import CategoryFakerBuilder


class TestEntitiesFakerBuilder(unittest.TestCase):
    
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