## Smoothie Shop

Author: Oliver Kaljuvee

#### Overview
Smoothie Shop is a demo RESTful application written in Python using Flask API.  The application exposes end-points 
to find products and ingredients.  The data gets loaded at startup from JSON files.  There is also an end-point to
add a product to the service (which is held in memory only).  

Another small feature is the ability to find products by filtering on the ingredient name:
```commandline
> curl http://localhost:5000/api/v1/products/filter.ingredient-name=Organic%20Banana
``` 
The lookup is done in constant time, i.e. `O(1)`, by pre-constructing a map of ingredients containing sets of products.  
  

#### Installing and Starting
These commands assume have installed Python 3.6+ (because the use of f-strings) and pip running on Windows:

```commandline
> python -m pip install --user virtualenv
> git clone https://github.com/okaljuvee/SmoothieShop.git
> cd SmoothieShop
> python -m venv venv
> .\venv\Scripts\activate
(venv) > pip install -r requirements.txt
(venv) > python app.py
```
**Important**: Do not use `flask run` command because it will not call the main entry point of `app.py` which does some required bootstrapping for the application.
#### Running
* View Products (all and by ID)
```commandline
> curl http://localhost:5000/api/v1/products
> curl http://localhost:5000/api/v1/products/3
```
* Create Products

To create a new smoothie (note that there is no POST end-point for ingredient creation):
```commandline
> curl -d "{\"id\":7,\"name\":\"Foo + Bar\",\"collection\": \"funky\",\"ingredient_ids\":[1,2,3]}" -H "Content-Type: application/json" http://localhost:5000/api/v1/products
```
**Important**: The content type is required in the header: `"Content-Type: application/json"`.  For better readability, the body of the example payload is:
```json
{
    "id": 7,
    "name": "Foo + Bar",
    "collection": "funky",
    "ingredient_ids": [
        1,
        2,
        3
    ]
}
```
You can confirm that the new smoothie got added to the service by using GET verb again:
```commandline
> curl http://localhost:5000/api/v1/products/7
```
* Find Products by Ingredient Name
```commandline
> curl http://localhost:5000/api/v1/products/filter.ingredient-name=Organic%20Banana
``` 
* Find Ingredients (all and by ID)
```commandline
> curl http://localhost:5000/api/v1/ingredients
> curl http://localhost:5000/api/v1/ingredients/3
```
### Tests
There is a single test for testing the lookup by ingredient:
```commandline
(venv) > python -m unittest test.product
```