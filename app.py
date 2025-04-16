from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# Dizionario per memorizzare gli shortlink
shortlinks = {}

# Funzione per generare un codice shortlink casuale
def generate_shortlink():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

@app.route('/create', methods=['GET'])
def create_shortlink():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    # Genera un shortlink e lo memorizza
    short_code = generate_shortlink()
    shortlinks[short_code] = url
    
    # Restituisce il shortlink
    return jsonify({"short_url": f"https://naviganti.wine/{short_code}"}), 200

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    url = shortlinks.get(short_code)
    
    if not url:
        return jsonify({"error": "Shortlink not found"}), 404

    return jsonify({"url": url}), 302

if __name__ == '__main__':
    # Aggiunto il parametro host='0.0.0.0' per Render
    app.run(host="0.0.0.0", port=5000, debug=False)
