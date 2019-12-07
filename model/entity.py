from typing import Dict, List, Any
from json import JSONEncoder
import json


class Entity:
    def __init__(self, **entries: Dict[str, Any]) -> None:
        self.__dict__.update(entries)

    @property
    def id(self) -> int:
        return self.__dict__.get('id')

    @property
    def name(self) -> str:
        return self.__dict__.get('name')

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, o):
        return self.__class__ == o.__class__ and self.id == o.id


class EntityEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Product(Entity):
    @property
    def collection(self) -> str:
        return self.__dict__.get('collection')

    @property
    def ingredient_ids(self) -> List[int]:
        return self.__dict__.get('ingredient_ids')


class Ingredient(Entity):
    @property
    def is_allergen(self) -> bool:
        return self.__dict__.get('is_allergen')
