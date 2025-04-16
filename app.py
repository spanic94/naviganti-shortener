from flask import Flask, redirect, request, jsonify
import string
import random
import json
import os

app = Flask(__name__)
DB_FILE = 'shortlinks.json'

if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as f:
        shortlinks = json.load(f)
else:
    shortlinks = {}

def save_db():
    with open(DB_FILE, 'w') as f:
        json.dump(shortlinks, f)

def generate_code(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/create')
def create():
    original_url = request.args.get('url')
    if not original_url:
        return "Parametro 'url' mancante", 400

    for code, link in shortlinks.items():
        if link == original_url:
            return jsonify(short_url=f"https://naviganti.wine/{code}")

    code = generate_code()
    while code in shortlinks:
        code = generate_code()

    shortlinks[code] = original_url
    save_db()
    return jsonify(short_url=f"https://naviganti.wine/{code}")

@app.route('/<code>')
def go(code):
    target = shortlinks.get(code)
    if target:
        return redirect(target)
    return "Link non trovato", 404

@app.route('/')
def home():
    return "Benvenuto nel tuo URL shortener ✂️"

if __name__ == '__main__':
    app.run()
