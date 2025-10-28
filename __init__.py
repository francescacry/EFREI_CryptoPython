from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(_name_)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
                                                                                                                                                     
if _name_ == "_main_":
  app.run(debug=True)
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
