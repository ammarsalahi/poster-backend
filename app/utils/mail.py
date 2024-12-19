from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from jinja2 import Environment,FileSystemLoader
import aiosmtplib
from app.core.config import settings


jinja2_env = Environment(loader=FileSystemLoader("templates"))
template=jinja2_env.get_template("email.html")

async def send_validation_email(email:EmailStr,code:str):
    template_data={
        "code":code
    }
    html_content=template.render(template_data)
    try:
        msg=MIMEText(html_content,"html")
        msg["From"] = settings.SMTP_USERNAME
        msg["To"] = email
        msg["Subject"] = "Poster Validation"
        smtp = SMTP(hostname=settings.SMTP_HOST,port=settings.SMTP_PORT)
        await smtp.connect()
        await smtp.starttls()
        await smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        await smtp.send_message(msg)
        await smtp.quit()


    #sending email
    # try:
    #     await aiosmtplib.send(
    #         message=msg,
    #         hostname=SMTP_HOST,
    #         username=SMTP_USERNAME,
    #         password=SMTP_PASSWORD,
    #         use_tls=True
    #     )
    except aiosmtplib.SMTPException as e:
        print(f"error:{str(e)}")
