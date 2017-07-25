import logging

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG = logging.getLogger(__name__)

EMAIL = 'auth.eubrabigsea@gmail.com'
EMAIL_PWD = 'Serverbigsea2017'

class SendEmail:

    def __init__(self):
        pass

    def send_email(self, email, subject, text):
        """
        Send email.
        """
        gmail_user = EMAIL
        gmail_pwd = EMAIL_PWD
        FROM = EMAIL
        TO = email
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, TO, subject, text)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            LOG.info('successfully sent the mail')
        except:
            LOG.info('failed to send mail')

    def send_email_with_token(self, username, email, token):
        """
        Send email with token.
        """
        CONFIRM_EMAIL_PATH = 'https://eubrabigsea.dei.uc.pt/web/email_confirmation'
        #CONFIRM_EMAIL_PATH = 'http://localhost:9000/web/email_confirmation'
        URL = CONFIRM_EMAIL_PATH + '?username='+username+'&email='+email+'&token='+token
        SUBJECT = 'EUBRA-BigSea: email confirmation'
        #TEXT = 'token: ' + token
        TEXT = 'Click on the following link to confirm the email:\n' + URL 

        return self.send_email(email, SUBJECT, TEXT)        
