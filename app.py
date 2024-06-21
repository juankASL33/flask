import os
from flask import Flask, render_template, request, redirect, url_for, abort
import json

app = Flask(__name__)

# Cargar datos del archivo JSON
with open('data.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query').lower()
        ingredient_type = request.form.get('ingredient_type')
        results = [
            recipe for recipe in data
            if query in recipe['name'].lower() and
            (ingredient_type in [i['type'] for i in recipe['ingredients']] if ingredient_type else True)
        ]
        return render_template('list.html', recipes=results)
    return render_template('search.html')

@app.route('/list_recipes', methods=['GET', 'POST'])
def list_recipes():
    if request.method == 'POST':
        query = request.form.get('query', '').lower()
        results = [recipe for recipe in data if query in recipe['name'].lower()]
        return render_template('list.html', recipes=results)
    return render_template('list.html', recipes=data)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipe = next((item for item in data if item['id'] == recipe_id), None)
    if recipe is None:
        abort(404)
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
