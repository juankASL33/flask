from flask import Flask, render_template, request, redirect, url_for, abort
import json

const express = require('express')
const app = express()
const port = process.env.PORT || 4000;

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
        results = [recipe for recipe in data if query in recipe['name'].lower()]
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
    app.run(debug=True)
