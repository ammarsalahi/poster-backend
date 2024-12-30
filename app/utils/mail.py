from aiosmtplib import SMTP
from email.mime.text import MIMEText
from pydantic import EmailStr
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings

# Initialize the Jinja2 environment
jinja2_env = Environment(loader=FileSystemLoader("templates"))
template = jinja2_env.get_template("email.html")

async def send_validation_email(email: EmailStr, code: str):
    # Prepare the template data and render the HTML content
    template_data = {"code": code}
    html_content = template.render(template_data)

    try:
        # Construct the email message
        msg = MIMEText(html_content, "html")
        msg["From"] = settings.SMTP_USERNAME
        msg["To"] = email
        msg["Subject"] = "Poster Validation"

        # Set up the SMTP connection
        async with SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
            await smtp.connect()
            await smtp.starttls()
            await smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

            # Send the email
            await smtp.send_message(msg)

    except aiosmtplib.SMTPException as e:
        # Log or handle the error appropriately
        print(f"Error sending email: {str(e)}")
        from aiosmtplib import SMTP
        from email.mime.text import MIMEText
        from pydantic import EmailStr
        from jinja2 import Environment, FileSystemLoader
        from app.core.config import settings

        # Initialize the Jinja2 environment
        jinja2_env = Environment(loader=FileSystemLoader("templates"))
        template = jinja2_env.get_template("email.html")

        async def send_validation_email(email: EmailStr, code: str):
            """
            Sends a validation email to the provided email address with the given code.

            Args:
                email (EmailStr): The recipient's email address.
                code (str): The validation code to include in the email.

            Returns:
                None
            """
            # Prepare the template data and render the HTML content
            template_data = {"code": code}
            html_content = template.render(template_data)

            try:
                # Construct the email message
                msg = MIMEText(html_content, "html")
                msg["From"] = settings.SMTP_USERNAME
                msg["To"] = email
                msg["Subject"] = "Poster Validation"

                # Set up the SMTP connection
                async with SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
                    await smtp.connect()
                    await smtp.starttls()
                    await smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

                    # Send the email
                    await smtp.send_message(msg)

            except aiosmtplib.SMTPException as e:
                # Log or handle the error appropriately
                print(f"Error sending email: {str(e)}")
