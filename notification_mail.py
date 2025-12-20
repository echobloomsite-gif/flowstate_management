from email.message import EmailMessage
import smtplib


def send_mail(From,to,content,Subject):
    message = EmailMessage()
    message['From'] = From
    message['To'] = to
    message['Subject'] = Subject
    message.set_content(content)

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(From,"jfir swho dezc ofad")
            server.send_message(message)
            print("Email_Envoyé avec succès ")
    except Exception as e:
        print("Une Erreur s'est produite lors du process de notification \nDetails:",e)



