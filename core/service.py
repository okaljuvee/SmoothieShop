from typing import Dict, List, Set, Any
from model.entity import Product, Ingredient, Entity
import json


class SmoothieService:
    """Service for managing smoothie products and ingredients"""
    def __init__(self, **kwargs):
        """
        Constructs the service.
        :param kwargs: Optional file paths to products and ingredients
        """
        if kwargs:
            self.path_products = kwargs.get('path_products')
            self.path_ingredients = kwargs.get('path_ingredients')
        # Dictionaries keyd by entity identifiers
        self.products = dict()
        self.ingredients = dict()
        # Contains product sets keyed by ingredient name
        self.ingredient_name_product_dict = dict()

    def add_product(self, product_json: Dict[str, Any]) -> List[Entity]:
        """
        Add a product to the service dictionary.
        :param product_json: JSON describing product
        :return: List of products successfully added to the service
        """
        product = Product(**product_json)
        self.products[product.id] = product
        self._update_name_lookup({product.id: product})
        return [product]

    def add_ingredient(self, ingredient_json: Dict[str, Any]) -> List[Entity]:
        """
        Add an ingredient to the service dictionary.
        :param ingredient_json: JSON describing ingredient
        :return: List of ingredient successfully added to the service
        """
        ingredient = Ingredient(**ingredient_json)
        self.ingredients[ingredient.id] = ingredient
        return [ingredient]

    def find_products(self, ingredient_name: str) -> Set[Product]:
        """
        Find products that contain the ingredient by name
        :param ingredient_name: Ingredient name to be searched in product list
        :return: Product set of products containing the ingredient, empty set otherwise
        """
        if ingredient_name in self.ingredient_name_product_dict:
            return self.ingredient_name_product_dict[ingredient_name]
        else:
            return set()

    def load_data(self) -> None:
        """
        Loads products and ingredients from JSON files and stores contents in dictionaries.
        :return: None
        """
        with open(self.path_products) as json_file:
            for product_dict in json.load(json_file)['products']:
                self.products[product_dict['id']] = Product(**product_dict)

        with open(self.path_ingredients) as json_file:
            for ingredient_dict in json.load(json_file)['ingredients']:
                self.ingredients[ingredient_dict['id']] = Ingredient(**ingredient_dict)

        print(f'Loaded {len(self.products)} products and {len(self.ingredients)} ingredients...')
        self._update_name_lookup(self.products)

    def _update_name_lookup(self, product_dict: Dict[int, Product]) -> None:
        """
        Convenience method that creates a dictionary of products keyed by ingredient names, which ensures O(1) lookup
        for all product searches by ingredient name.
        :return: None
        """
        for product in product_dict.values():
            for ingredient_id in product.ingredient_ids:
                ingredient = self.ingredients[ingredient_id]
                product_set = self.ingredient_name_product_dict.get(ingredient.name, set())
                product_set.add(product)
                self.ingredient_name_product_dict[ingredient.name] = product_set
