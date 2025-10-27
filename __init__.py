from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet, InvalidToken
import base64

app = Flask(__name__)

def generate_key_from_user_input(user_key: str):
    """
    Transforme la clé saisie par l'utilisateur en une clé compatible avec Fernet.
    """
    key = user_key.encode('utf-8')
    key = key.ljust(32, b'0')[:32]  # ajuste à 32 octets
    return base64.urlsafe_b64encode(key)

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur l’API CryptoPython !",
        "routes_disponibles": ["/encrypt/", "/decrypt/"]
    })

@app.route('/encrypt/', methods=['POST'])
def encrypt():
    """
    Chiffre un texte en utilisant la clé fournie par l'utilisateur.
    """
    data = request.json
    text = data.get('text')
    user_key = data.get('key')

    if not text or not user_key:
        return jsonify({'error': 'Veuillez fournir un texte et une clé.'}), 400

    try:
        key = generate_key_from_user_input(user_key)
        cipher = Fernet(key)
        encrypted_text = cipher.encrypt(text.encode())
        return jsonify({'encrypted_text': encrypted_text.decode()})
    except Exception as e:
        return jsonify({'error': 'Erreur lors du chiffrement', 'details': str(e)}), 500

@app.route('/decrypt/', methods=['POST'])
def decrypt():
    """
    Déchiffre un texte chiffré en utilisant la clé fournie par l'utilisateur.
    """
    data = request.json
    encrypted_text = data.get('encrypted_text')
    user_key = data.get('key')

    if not encrypted_text or not user_key:
        return jsonify({'error': 'Veuillez fournir un texte chiffré et une clé.'}), 400

    try:
        key = generate_key_from_user_input(user_key)
        cipher = Fernet(key)
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
        return jsonify({'decrypted_text': decrypted_text})
    except InvalidToken:
        return jsonify({'error': 'Clé incorrecte ou texte invalide.'}), 400
    except Exception as e:
        return jsonify({'error': 'Erreur lors du décryptage', 'details': str(e)}), 500
