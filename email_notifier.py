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
    self.EMAIL_SERVER = os.getenv('EMAIL_SERVER')
    self.EMAIL_PORT = os.getenv('EMAIL_PORT')

    logging.info('EMAIL_SENDER = {0}'.format(self.EMAIL_SENDER))
    logging.info('EMAIL_RECEIVER = {0}'.format(self.EMAIL_RECEIVER))
    logging.info('EMAIL_SERVER = {0}'.format(self.EMAIL_SERVER))
    logging.info('EMAIL_PORT = {0}'.format(self.EMAIL_PORT))

  def send_message(self, message):
    logging.info('Sending EMAIL notification')
    logging.debug('message = {0}'.format(message))
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    try:
      with smtplib.SMTP_SSL(self.EMAIL_SERVER, self.EMAIL_PORT, context=context) as server:
        server.login(self.EMAIL_LOGIN, self.EMAIL_PWD)
        not_delivered = server.sendmail(self.EMAIL_SENDER, self.EMAIL_RECEIVER, message)

        if not_delivered:
          raise Exception('Email notification was not delivered properly. Undelivered to {0}'.format(json.dumps(not_delivered)))
        else:
          logging.info('EMAIL notification sent')
    except Exception as e:
      logging.exception(e)
      return False
    
    return True

      
