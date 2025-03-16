import asyncio
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import get_settings

settings = get_settings()

# Configure logger
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = settings.SENDGRID_FROM_EMAIL
    
    DEFAULT_TEMPLATE = """
    <html>
        <body>
            <h1>{subject}</h1>
            <p>{content}</p>
            <p>Regards,<br>Your Team</p>
        </body>
    </html>
    """
    
    async def send_email(self, to_emails: list, subject: str, content: str):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=self.DEFAULT_TEMPLATE.format(subject=subject, content=content)
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Email sent successfully. Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
        await asyncio.sleep(0.1)