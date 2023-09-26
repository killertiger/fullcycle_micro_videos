import unittest
from core.category.domain.entities_faker_builder import CategoryFakerBuilder


class TestEntitiesFakerBuilder(unittest.TestCase):
    
    def test_build(self):
        print(CategoryFakerBuilder.a_category().build())