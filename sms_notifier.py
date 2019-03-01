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

      logging.debug('send_result = {0}'.format(send_result))
      logging.debug('text = {0}'.format(message))
      # response example: {"message-count": "1", "messages": [{"to": "420735159055", "message-id": "140000000BB24AD0", "status": "0", "remaining-balance": "1.72820000", "message-price": "0.04530000", "network": "23001"}]}
      # error example: {'message-count': '1', 'messages': [{'to': '420604346762', 'status': '29', 'error-text': 'Non White-listed Destination - rejected'}]}
      message_result = send_result['messages'][0]
      status = message_result['status']

      if (status == '0'):
        remaining_balance = float(message_result['remaining-balance'])
        logging.info('Remaining balance: {0}'.format(remaining_balance))

        if remaining_balance < 0.5:
          logging.warning('Nexmo remaining balance too low!!! Remaining balance: {0}'.format(remaining_balance))

        logging.info('SMS Nofitication sent.')

      else:
        logging.error('Something went wrong during sending SMS: {0}'.format(send_result))

      
    except Exception as e:
      logging.error(e)
      return False

    return True