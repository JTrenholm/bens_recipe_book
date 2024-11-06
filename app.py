from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests
import logging

app = Flask(__name__)

# Spoonacular API credentials
API_KEY = "1c24c606dd5d4dca87b51c818446cd16"  # Replace with your actual API_KEY

# Database connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create favorites table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY,
        recipe_id INTEGER,
        name TEXT,
        image TEXT
    );
""")
conn.commit()

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Index page endpoint
@app.route('/')
def index():
    return render_template('index.html')

# Recipe search endpoint
@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('query')
    cuisine = request.args.get('cuisine')
    ingredient = request.args.get('ingredient')
    surprise = request.args.get('surprise')

    if surprise:
        api_url = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&number=1'
        try:
            logging.info(f"API Request URL: {api_url}")
            response = requests.get(api_url)
            response.raise_for_status()
            logging.info(f"API Response Status Code: {response.status_code}")
            recipe = response.json()
            logging.info(f"Recipe: {recipe}")

            # Check if 'id' key exists
            if 'id' in recipe:
                return redirect(url_for('recipe_details', recipe_id=recipe['id']))
            else:
                error = "Recipe ID missing"
                logging.error(error)
                return render_template('error.html', error=error)
        except requests.exceptions.RequestException as e:
            error = str(e)
            logging.error(f"API Request Failed: {error}")
            return render_template('error.html', error="API Request Failed")
        except Exception as e:
            error = str(e)
            logging.error(f"Internal Server Error: {error}")
            return render_template('error.html', error="Internal Server Error")
    elif cuisine:
        api_url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&cuisine={cuisine}&number=10'
    elif ingredient:
        api_url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&ingredients={ingredient}&number=10'
    else:
        api_url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={query}&number=10'

    try:
        logging.info(f"API Request URL: {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()
        logging.info(f"API Response Status Code: {response.status_code}")
        recipes = response.json()['results']
        return render_template('index.html', recipes=recipes)
    except requests.exceptions.RequestException as e:
        error = str(e)
        logging.error(f"API Request Failed: {error}")
        return render_template('error.html', error="API Request Failed")
    except Exception as e:
        error = str(e)
        logging.error(f"Internal Server Error: {error}")
        return render_template('error.html', error="Internal Server Error")

# Recipe details endpoint
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_details(recipe_id):
    api_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}&includeNutrition=false'
    try:
        logging.info(f"API Request URL: {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()
        logging.info(f"API Response Status Code: {response.status_code}")
        recipe = response.json()
        return render_template('recipe.html', recipe=recipe)
    except requests.exceptions.RequestException as e:
        error = str(e)
        logging.error(f"API Request Failed: {error}")
        return render_template('error.html', error="API Request Failed")
    except Exception as e:
        error = str(e)
        logging.error(f"Internal Server Error: {error}")
        return render_template('error.html', error="Internal Server Error")

# Favorite recipe endpoint
@app.route('/favorite', methods=['POST'])
def add_favorite():
    logging.info("Adding favorite recipe")
    recipe_id = int(request.form['recipe_id'])
    name = request.form['name']
    image = request.form['image']

    cursor.execute("INSERT INTO favorites (recipe_id, name, image) VALUES (?, ?, ?)", (recipe_id, name, image))
    conn.commit()
    logging.info("Recipe added to favorites")

    return redirect(url_for('favorites'))

# Favorites page endpoint
@app.route('/favorites', methods=['GET'])
def favorites():
    cursor.execute("SELECT * FROM favorites")
    favorites = cursor.fetchall()

    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        conn.close()