import os

from flask import Flask,jsonify,request
from flask_cors import CORS
from pyairtable import Table
import uuid
import hashlib
import datetime
app = Flask(__name__)
CORS(app)

#DATABASE PARAMETER
Api_key = os.getenv("AIRTABLE_API_KEY")
Base_Id = os.getenv("AIRTABLE_BASE_ID")
Table_data = os.getenv("AIRTABLE_TABLE_NAME")

init_Table = Table(Api_key,Base_Id,Table_data)
read_table = init_Table.all()
@app.route("/get_auth",methods=['POST'])
def get_date():
    get_data = request.get_json()
    #Get Primordial DATA
    mail = get_data['email']
    constitute_dict = {
        "USER_UUID":str(uuid.uuid4()),
        "mail":get_data['email'],
        "password":hashlib.sha256(get_data['password'].encode()).hexdigest(),
        "Username":get_data['full_name'],
        "Initial Role":get_data['initial_titre'],
        "initial_revenue":get_data['initial_revenue'],
        "initial_team_size":get_data['initial_team_size'],
        "initial_client_count":get_data['initial_client_count'],
        "created_date":str(datetime.datetime.now()),
        "last_log_date": str(datetime.datetime.now())
    }
    print(constitute_dict)
    #SAVING PART LOGICAL
    # Vérifier si l'email existe déjà
    for data in read_table:
        fields = data.get('fields', {})
        if fields.get('mail') == constitute_dict["mail"]:
            print("Email déjà utilisé")
            return jsonify({'status': False, 'message': 'Email déjà utilisé'})

    # Si aucun email trouvé → créer
    try:
        init_Table.create(constitute_dict)
        print("SUCCESS")
        return jsonify({'status': True})
    except Exception as e:
        print("Error:", e)
        return jsonify({'status': False, 'error': str(e)})
