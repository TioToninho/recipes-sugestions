from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/recipes")
async def recipes(request: Request, ingredients: str = Form(...)):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients,
        'number': 10,
        'apiKey': 'YOUR_API_KEY',
    }
    response = requests.get(url, params=params)

    if response.ok:
        recipes = response.json()
        if len(recipes) > 0:
            recipe = random.choice(recipes)
            return templates.TemplateResponse(
                "recipes.html", {"request": request, "recipe": recipe}
            )
        else:
            return templates.TemplateResponse("no-recipes.html", {"request": request})
    else:
        return templates.TemplateResponse("error.html", {"request": request})
