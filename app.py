import logging
import logging.handlers
import time
from timeloop import Timeloop
from datetime import timedelta
import datetime
import configparser
from dotenv import load_dotenv
import os

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(module)s:%(message)s'
formatter = logging.Formatter(LOG_FORMAT)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

# File logging
file_handler = logging.handlers.RotatingFileHandler('hydroNotifier.log', mode='a', maxBytes=1000000, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logging.getLogger('').addHandler(file_handler)

# Console logging
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)
# logging.getLogger('').addHandler(console_handler)
# logger.addHandler(console_handler)

# SMTP logging
# load_dotenv('.env', verbose=True)

# # Load in configuration from environment variables:
# EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
# EMAIL_PWD = os.getenv('EMAIL_PWD')
# EMAIL_SERVER=os.getenv('EMAIL_SERVER')
# EMAIL_LOGGING_PORT=os.getenv('EMAIL_LOGGING_PORT')

# smtp_handler = logging.handlers.SMTPHandler(
#   mailhost=(EMAIL_SERVER, EMAIL_LOGGING_PORT),
#   fromaddr='ledvinka.david@gmail.com',
#   toaddrs=['ledvinka.david@gmail.com'],
#   subject='HydroNotifier - Application error',
#   credentials=(EMAIL_LOGIN, EMAIL_PWD),
#   secure=(),
#   timeout=30.0)

# smtp_handler.setLevel(logging.WARNING)
# smtp_handler.setFormatter(formatter)
# logging.getLogger('').addHandler(smtp_handler)

logging.info('HydroNotifier started')
# logging.error('SMTP test')

from email_notifier import EmailNotifier
from sms_notifier import SmsNotifier
from data_scrapper import DataScrapper
from message_formatter import MessageFormatter, LimitType

limit_low_signalled = False
limit_high_signalled = False

tl = Timeloop()
ds = DataScrapper()
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
message_formatter = MessageFormatter()

config = configparser.ConfigParser()
config.read('config.ini')
LEVEL_LOW = config['LEVELS']['LevelLow']
LEVEL_HIGH = config['LEVELS']['LevelHigh']

logging.info('LEVEL_LOW = {0}'.format(LEVEL_LOW))
logging.info('LEVEL_HIGH = {0}'.format(LEVEL_HIGH))

@tl.job(interval=timedelta(seconds=5))
def main_job():
  logging.debug('Job started')

  values = ds.get_values()

  if len(values) == 2:
    (date_lomna, flow_lomna) = values['Lomna']
    (date_olse, flow_olse) = values['Olse']

    flow_sum = flow_lomna + flow_olse

    global limit_low_signalled, limit_high_signalled

    if (flow_sum < LEVEL_LOW and not limit_low_signalled):
      notifications_sent = send_notifications(flow_sum, flow_lomna, flow_olse, date_lomna, date_olse, LimitType.LOW)

      if True in notifications_sent:
        limit_low_signalled = True
        limit_high_signalled = False

    if (flow_sum > LEVEL_HIGH and not limit_high_signalled):
      notifications_sent = send_notifications(flow_sum, flow_lomna, flow_olse, date_lomna, date_olse, LimitType.LOW)

      if True in notifications_sent:
        limit_low_signalled = False
        limit_high_signalled = True


def send_notifications(flow_sum, flow_lomna, flow_olse, date_lomna, date_olse, limit_type):
  email_message = message_formatter.get_email_message(flow_sum, flow_lomna, flow_olse, date_lomna, date_olse, limit_type)
  email_sent = email_notifier.send_message(email_message)
  sms_message = message_formatter.get_sms_message(flow_sum, limit_type)
  sms_sent = sms_notifier.send_message(sms_message)
  return [email_sent, sms_sent]


if __name__ == "__main__":
  #tl.start(block=True)
  logging.info('HydroNotifier stopped')
