import os

from flask import Flask,jsonify,request
from flask_cors import CORS
from pyairtable import Table
import uuid
import hashlib
from email.message import EmailMessage
import smtplib
import datetime
app = Flask(__name__)
CORS(app)
created = False
#DATABASE PARAMETER
Api_key = os.getenv("AIRTABLE_API_KEY")
Base_Id = os.getenv("AIRTABLE_BASE_ID")
Table_data = os.getenv("AIRTABLE_TABLE_NAME")
collaborator_email_list = ["echobloomsite@gmail.com","matheoestrela@gmail.com","lawrenceguerrier@gmail.com","jerome.damien.dj@gmail.com"]
init_Table = Table(Api_key,Base_Id,Table_data)
read_table = init_Table.all()

def send_mail(From,to,content,Subject):
    message = EmailMessage()
    message['From'] = From
    message['To'] = to
    message['Subject'] = Subject
    message.set_content(content)

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(From,os.getenv("EMAIL_PASSWORD"))
            server.send_message(message)
            print("Email_Envoyé avec succès ")
    except Exception as e:
        print("Une Erreur s'est produite lors du process de notification \nDetails:",e)
@app.route("/get_auth", methods=["POST"])
def get_date():
    try:
        get_data = request.get_json(force=True)

        constitute_dict = {
            "USER_UUID": str(uuid.uuid4()),
            "mail": get_data["email"],
            "password": hashlib.sha256(get_data["password"].encode()).hexdigest(),
            "Username": get_data["full_name"],
            "Initial Role": get_data["initial_titre"],
            "initial_revenue": get_data["initial_revenue"],
            "initial_team_size": get_data["initial_team_size"],
            "initial_client_count": get_data["initial_client_count"],
            "created_date": str(datetime.datetime.now()),
            "last_log_date": str(datetime.datetime.now())
        }

        # Vérification email
        records = init_Table.all()
        for data in records:
            if data.get("fields", {}).get("mail") == constitute_dict["mail"]:
                return jsonify({"status": False, "message": "Email déjà utilisé"}), 409

        # Création utilisateur
        init_Table.create(constitute_dict)
        print("USER CREATED")

        # Notification (non bloquante)
        message = f"""
Bonjour,

Nouvelle inscription sur Flowstate.

Nom : {get_data['full_name']}
Email : {get_data['email']}
Rôle : {get_data['initial_titre']}

Date : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}

— Flowstate
"""

        for collaborator in collaborator_email_list:
            try:
                send_mail(
                    "flowstate.os.sup@gmail.com",
                    collaborator,
                    message,
                    "[Flowstate] Nouvelle inscription utilisateur"
                )
            except Exception as mail_error:
                print("MAIL ERROR (ignored):", mail_error)

        # 🔥 RÉPONSE GARANTIE
        return jsonify({"status": True}), 201

    except Exception as e:
        print("FATAL ERROR:", e)
        return jsonify({"status": False, "error": "Internal server error"}), 500
