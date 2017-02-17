from flask_mail import Message
from project import app
import config
from project.core import mail

def send_email(to, subject, template):
    msg = Message(
    subject,
    recipients=[to],
    html=template,
    sender=app.config.from_object(config.DevelopmentConfig)
    )
    mail.send(msg)