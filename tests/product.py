import unittest
from core.service import SmoothieService


class TestProducts(unittest.TestCase):

    def test_find_products_by_name(self):
        """
        Test for finding products by ingredient name
        """
        service = SmoothieService()
        product_set = service.find_products("Foo")
        self.assertEqual(len(product_set), 0)
        self.populate_test_data(service)
        product_set = service.find_products("Foo")
        self.assertEqual(product_set.pop().ingredient_ids[0], 1)
        product_set = service.find_products("Bar")
        self.assertEqual(len(product_set), 0)

    @staticmethod
    def populate_test_data(service):
        service.add_ingredient({
            "id": 1,
            "name": "Foo",
            "is_allergen": False
        })
        service.add_ingredient({
            "id": 2,
            "name": "Bar",
            "is_allergen": False
        })
        service.add_product({
            "id": 1,
            "name": "Foo - Bar",
            "collection": "test",
            "ingredient_ids": [
                1
            ]
        })
        service._create_name_lookup()


if __name__ == '__main__':
    unittest.main()
