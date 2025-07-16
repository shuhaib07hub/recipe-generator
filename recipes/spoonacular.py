import requests

API_KEY = '40a9a2670c4a49438d4fad2b424a0bc7'
BASE_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

def get_recipes_by_ingredients(ingredients):
    params = {
        'ingredients': ingredients,
        'number': 5,  # number of recipes
        'apiKey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()  # returns list of recipes
    return []
