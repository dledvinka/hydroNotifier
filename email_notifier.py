from dotenv import load_dotenv
import nexmo
import os
import logging
import smtplib, ssl
import json

class EmailNotifier:
  def __init__(self):
    # Load environment variables from a .env file:
    load_dotenv('.env', verbose=True)
    
    # Load in configuration from environment variables:
    self.EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
    self.EMAIL_PWD = os.getenv('EMAIL_PWD')
    self.EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    self.EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
    self.EMAIL_SERVER = os.getenv('EMAIL_RECEIVER')
    self.EMAIL_PORT = os.getenv('EMAIL_RECEIVER')

    logging.info('NEXMO_API_KEY = {0}'.format(self.EMAIL_SENDER))
    logging.info('NEXMO_API_KEY = {0}'.format(self.EMAIL_RECEIVER))
    logging.info('NEXMO_API_KEY = {0}'.format(self.EMAIL_SERVER))
    logging.info('NEXMO_API_KEY = {0}'.format(self.EMAIL_PORT))

  def send_message(self, message):
    logging.info('Sending EMAIL notification')
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(self.EMAIL_SERVER, self.EMAIL_PORT, context=context) as server:
      try:
        server.login(self.EMAIL_LOGIN, self.EMAIL_PWD)
        not_delivered = server.sendmail(self.EMAIL_SENDER, self.EMAIL_RECEIVER, message)

        if not not_delivered:
          raise Exception('Email notification was not delivered properly. Undelivered to {not_delivered}'.format(json.dumps(not_delivered)))
        else:
          logging.info('EMAIL notification sent')
      except Exception as e:
        logging.exception(e)
        return False
      finally:
        server.quit()
    
    return True

      
