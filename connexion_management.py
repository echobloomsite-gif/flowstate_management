from flask import Flask,jsonify,request
from flask_cors import CORS
from pyairtable import Table
import hashlib
import os
import datetime
app = Flask(__name__)
CORS(app)

#DATABASE PARAMETER
Api_key = os.getenv("AIRTABLE_API_KEY")
Base_Id = os.getenv("AIRTABLE_BASE_ID")
Table_data = os.getenv("AIRTABLE_TABLE_NAME")

init_Table = Table(Api_key,Base_Id,Table_data)
read_table = init_Table.all()
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    mail = data.get('email')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()

    if not mail or not password:
        return jsonify({
            'status': False,
            'message': 'Email ou mot de passe manquant'
        }), 400

    for record in read_table:
        fields = record.get('fields', {})

        # Vérifier si l'email correspond
        if fields.get('mail') == mail:

            # Vérifier le mot de passe
            if fields.get('password') == password:
                init_Table.create({"last_log_date":str(datetime.datetime.now())})
                return jsonify({
                    'status': True,
                    'message': 'Connexion réussie'
                }), 200
            else:
                return jsonify({
                    'status': False,
                    'message': 'Mot de passe incorrect'
                }), 401

    # Aucun email trouvé
    return jsonify({
        'status': False,
        'message': 'Utilisateur introuvable'
    }), 404

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5555,debug=True)