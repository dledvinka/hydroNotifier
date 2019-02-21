from dotenv import load_dotenv
import nexmo
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('sms.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def send_text_message():
  # Load environment variables from a .env file:
  load_dotenv('.env', verbose=True)
  
  # Load in configuration from environment variables:
  NEXMO_API_KEY = os.getenv('NEXMO_API_KEY')
  NEXMO_API_SECRET = os.getenv('NEXMO_API_SECRET')
  SMS_TO = os.getenv('SMS_TO')

  logger.info(NEXMO_API_KEY)
  logger.info(NEXMO_API_SECRET)
  logger.info(SMS_TO)

  client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

  send_result = client.send_message({
      'from': 'Nexmo',
      'to': SMS_TO,
      'text': 'Hello from HydroNotifier',
  })

  logger.info(send_result)

if __name__ == "__main__":
    send_text_message()
    logger.info('Program done.')