import unittest
from core.category.domain.entities_faker_builder import CategoryFakerBuilder


class TestEntitiesFakerBuilder(unittest.TestCase):
    
    def test_build(self):
        # tmp = CategoryFakerBuilder.a_category()
        # print(CategoryFakerBuilder.a_category().build())
        # print(CategoryFakerBuilder.the_categories(2).build())
        
        faker = CategoryFakerBuilder.the_categories(2)
        faker = faker.with_name(lambda index: 'Moaaaaaaaaa' + str(index))
        print(faker.build())
        print(faker.name)
        print(faker.name)
        print(faker.name)
        print(faker.name)