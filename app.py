from typing import List
from flask import Flask, jsonify, make_response, request
import json
from core.service import SmoothieService
from model.entity import EntityEncoder

HEADER = {"Content-Type": "application/json"}
app = Flask(__name__)
service = SmoothieService(path_products='resources/products.json', path_ingredients='resources/ingredients.json')


@app.route('/api/v1/products', methods=['GET'])
def get_products() -> str:
    return get_response('products', list(service.products.values()))


@app.route('/api/v1/products', methods=['POST'])
def create_product() -> str:
    product = service.add_product(request.json)
    return get_response('products', product, status=201)


@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int) -> str:
    products = [product for product in list(service.products.values()) if product.id == product_id]
    return not_found('Product not found') if len(products) == 0 else get_response('products', products)


@app.route('/api/v1/products/filter.<string:filter_key>=<string:filter_val>', methods=['GET'])
def find_product(filter_key: str, filter_val: str) -> str:
    if filter_key != 'ingredient-name':
        return make_response(jsonify({'error': 'Unsupported filter'}), 400)

    products = list(service.find_products(ingredient_name=filter_val))
    return not_found('Product not found') if len(products) == 0 else get_response('products', products)


@app.route('/api/v1/ingredients', methods=['GET'])
def get_ingredients() -> str:
    return get_response('ingredients', list(service.ingredients.values()))


@app.route('/api/v1/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id: int) -> str:
    ingredients = [ingredient for ingredient in list(service.ingredients.values()) if ingredient.id == ingredient_id]
    return not_found('Ingredient not found') if len(ingredients) == 0 else get_response('ingredients', ingredients)


def get_response(key: str, collection: List, status: int = 200) -> str:
    payload = dict()
    payload[key] = collection
    return make_response(json.dumps(payload, indent=4, cls=EntityEncoder), status, HEADER)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)


if __name__ == '__main__':
    service.load_data()
    app.run()
