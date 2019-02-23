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

      # response example: {"message-count": "1", "messages": [{"to": "420735159055", "message-id": "140000000BB24AD0", "status": "0", "remaining-balance": "1.72820000", "message-price": "0.04530000", "network": "23001"}]}
      remaining_balance = float(send_result['messages'][0]['remaining-balance'])
      logging.info('Remaining balance: {0}'.format(remaining_balance))

      if remaining_balance < 0.5:
        logging.warning('Nexmo remaining balance too low!!! Remaining balance: {0}'.format(remaining_balance))

      logging.info('SMS Nofitication sent, response: {0}'.format(json.dumps(send_result)))
    except Exception as e:
      logging.error(e)
      return False

    return True