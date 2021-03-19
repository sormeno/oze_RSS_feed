import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import logging
logger = logging.getLogger('RSS_feed.mail')

class SMTP:

    def __init__(self, host, port, msg_from, password):
        self.s = smtplib.SMTP(host=host, port=port)
        self.msg_from = msg_from
        self.s.starttls()
        self.s.ehlo()
        try:
            self.s.login(self.msg_from, password)
            self.s.ehlo()
            logger.info(f'Successful login to {self.msg_from}. Server response: {self.s.ehlo_resp}')
            logger.info(f'Server supports ESMTP: {self.s.does_esmtp}. SMTP server extensions: {self.s.esmtp_features}')
        except:
            logger.error(f'Failed to login to {self.msg_from}', exc_info=True)
            sys.exit()



    def close(self):
        try:
            self.s.ehlo()
            logger.info(f'Closing connection. Server response: {self.s.ehlo_resp}')
            self.s.quit()
            logger.info(f'Mail login to {self.msg_from} successfully closed. Server response: {self.s.ehlo_resp}')
        except Exception as e:
            logger.warning(f'Mail login to {self.msg_from} has not been closed with exception {e}', exc_info=True)


    def send_email(self,msg_to, msg_subject, msg_content = None, msg_html_content = None):
        msg = MIMEMultipart()
        msg_content = msg_html_content if msg_html_content else msg_content
        msg_type = 'html' if msg_html_content else 'plain'

        msg['From'] = self.msg_from
        msg['To'] = msg_to
        msg['Subject'] = msg_subject
        logger.info(f'Preparing message \'{msg["Subject"]}\' to \'{msg["To"]}\' from \'{msg["From"]}\'. Message type: {msg_type}')
        msg.attach(MIMEText(msg_content, msg_type))
        logger.info(f'Message content attached to message')
        self.s.ehlo()
        self.s.send_message(msg)
        logger.info(f'Message to \'{msg["To"]}\' has been sent. Server response: {self.s.ehlo_resp}')
        del msg


