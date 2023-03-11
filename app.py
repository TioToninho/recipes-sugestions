import logging
from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/recipes', methods=['POST'])
def recipes():
    ingredients = request.form['ingredients']
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients,
        'number': 10,
        'apiKey': 'API_KEY',
    }

    response = requests.get(url, params=params)
    if response.ok:
        recipes = response.json()
        if len(recipes) > 0:
            recipe = random.choice(recipes)
            print(recipe)
            return render_template('recipes.html', recipe=recipe)
        else:
            return render_template('no-recipes.html')
    else:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
