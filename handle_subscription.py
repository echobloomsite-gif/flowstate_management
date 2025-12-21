from flask_cors import CORS
from pyairtable import Table
from flask import Flask, jsonify, request
import os

Api_key = os.getenv("AIRTABLE_API_KEY")
Base_Id = os.getenv("AIRTABLE_BASE_ID")
Table_data = os.getenv("AIRTABLE_TABLE_NAME")
init_Table = Table(Api_key, Base_Id, Table_data)

app = Flask(__name__)
CORS(app)


@app.route("/check-payment", methods=["POST"])
def handling():
    try:
        datas = request.get_json()
        get_mail = datas.get('email')
        event_type = datas.get('event_type')

        if not get_mail:
            return jsonify({"status": False, "error": "Email missing"}), 400

        # Recherche optimisée avec formula au lieu de .all()
        records = init_Table.all(formula=f"{{mail}} = '{get_mail}'")

        if not records:
            print(f"No user found with email: {get_mail}")
            return jsonify({"status": False, "error": "User not found"}), 404

        record = records[0]
        record_id = record['id']

        # Mapping des event_type vers subscription status
        status_map = {
            "payment_success": "Active",
            "trial_ended": "Disabled",
            "payment_failed": "Payment_Failed",
            "trial_ending": "Trial_Ending"  # Avertissement
        }

        new_status = status_map.get(event_type, "Active")

        init_Table.update(record_id, {"subscription": new_status})
        print(f"Updated {get_mail} subscription to: {new_status}")

        return jsonify({"status": True, "subscription": new_status}), 200

    except Exception as e:
        print(f"Error processing payment webhook: {e}")
        return jsonify({"status": False, "error": str(e)}), 500


