from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List



conf = ConnectionConfig(
    MAIL_USERNAME = "vaibhavbn.acumenusa@gmail.com",
    MAIL_PASSWORD = "pfvb kfjy alho pish",
    MAIL_FROM = "vaibhavbn.acumenusa@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Task Management App",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(emails: List[str]): 
    html = """<p>Hi, Thanks for registration. Our team will connect with you soon.</p> """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent successfully"}