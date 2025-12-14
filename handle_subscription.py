from flask_cors import CORS
from pyairtable import Table
from flask import Flask,jsonify,request
import os

Api_key = os.getenv("AIRTABLE_API_KEY")
Base_Id = os.getenv("AIRTABLE_BASE_ID")
Table_data = os.getenv("AIRTABLE_TABLE_NAME")
init_Table = Table(Api_key, Base_Id, Table_data)

app = Flask(__name__)
CORS(app)
@app.route("/check-payment",methods=["POST"])
def handelign():
    datas = request.get_json()
    get_mail = datas['email']
    event_type = datas['event_type']
    if not get_mail:
        return jsonify({"status": False, "error": "Email missing"}), 400

    if event_type == "trial_ended":
        records = init_Table.all()
        try:
            for data in records:
                if get_mail in data['fields']['mail']:
                    get_records_id = data['id']
                    init_Table.update(get_records_id,{"subscription":"Done"})
                    return jsonify({"status": True}),200
        except Exception as e:
            print("Une erreur s'est produite lors du processus",e)
            return jsonify({"status": True}), 500
    else:
        records = init_Table.all()
        try:
            for data in records:
                if get_mail in data['fields']['mail']:
                    get_records_id = data['id']
                    init_Table.update(get_records_id,{"subscription":"Active"})
                    return jsonify({"status": True}), 200
        except Exception as e:
            print("Une erreur s'est produite lors du processus", e)
            return jsonify({"status": True}), 500
