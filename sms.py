from dotenv import load_dotenv
import nexmo
import os

def send_text_message():
  # Load environment variables from a .env file:
  load_dotenv('.env', verbose=True)
  
  # Load in configuration from environment variables:
  NEXMO_API_KEY = os.getenv('NEXMO_API_KEY')
  NEXMO_API_SECRET = os.getenv('NEXMO_API_SECRET')
  SMS_TO = os.getenv('SMS_TO')

  print(NEXMO_API_KEY)
  print(NEXMO_API_SECRET)
  print(SMS_TO)

  client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

  send_result = client.send_message({
      'from': 'Nexmo',
      'to': SMS_TO,
      'text': 'Hello from HydroNotifier',
  })

  print(send_result)

if __name__ == "__main__":
    send_text_message()
    print('Program done.')