from flask import Flask, jsonify, request
from flask_cors import CORS
from pyairtable import Table
import hashlib
import os
import datetime

app = Flask(__name__)
CORS(app)

# DATABASE
Api_key = os.getenv("AIRTABLE_API_KEY")
Base_Id = os.getenv("AIRTABLE_BASE_ID")
Table_data = os.getenv("AIRTABLE_TABLE_NAME")

init_Table = Table(Api_key, Base_Id, Table_data)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'status': False, 'message': 'Invalid JSON'}), 400

    mail = data.get('email')
    raw_password = data.get('password')

    if not mail or not raw_password:
        return jsonify({
            'status': False,
            'message': 'Email ou mot de passe manquant'
        }), 400

    hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()

    # Recharge la table à chaque requête
    records = init_Table.all()

    for record in records:
        fields = record.get('fields', {})

        if fields.get('mail') == mail:
            if fields.get('password') == hashed_password:

                # ✅ Update du user connecté
                init_Table.update(
                    record['id'],
                    {"last_log_date": str(datetime.datetime.now())}
                )

                return jsonify({
                    'status': True,
                    'message': 'Connexion réussie'
                }), 200
            else:
                return jsonify({
                    'status': False,
                    'message': 'Mot de passe incorrect'
                }), 401

    return jsonify({
        'status': False,
        'message': 'Utilisateur introuvable'
    }), 404
