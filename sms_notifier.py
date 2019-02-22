from dotenv import load_dotenv
import nexmo
import os
import logging
import json

class SmsNotifier:
  def __init__(self):
    # Load environment variables from a .env file:
    load_dotenv('.env', verbose=True)
    
    # Load in configuration from environment variables:
    self.NEXMO_API_KEY = os.getenv('NEXMO_API_KEY')
    self.NEXMO_API_SECRET = os.getenv('NEXMO_API_SECRET')
    self.SMS_TO = os.getenv('SMS_TO')

    logging.info('SMS_TO = {0}'.format(self.SMS_TO))

  def send_message(self, message):
    try:
      logging.info('Sending SMS notification')
      client = nexmo.Client(key=self.NEXMO_API_KEY, secret=self.NEXMO_API_SECRET)
      send_result = client.send_message({
          'from': 'HydroNotifier',
          'to': self.SMS_TO,
          'text': message,
      })
      logging.info('SMS Nofitication sent, response: {response}'.format(json.dumps(send_result)))
    except Exception as e:
      logging.error(e)
      return False

    return True