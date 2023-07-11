from typing import Optional
import unittest

from datetime import datetime
from category.application.dto import CategoryOutput

class TestCategoryOutput(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(CategoryOutput.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': bool,
            'created_at': datetime
        })