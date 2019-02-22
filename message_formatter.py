from enum import Enum
import datetime

class LimitType(Enum):
  LOW = 1,
  HIGH = 2

class MessageFormatter:
  def __inin__(self):
    pass
  
  def get_email_message(self, flow_sum, flow_lomna, flow_olse, date_lomna, date_olse, limit_type):
    return """\
Subject: Jablunkov MVE - {0}

Lomna:
Datum a cas: {1}
Prutok [l/s]: {2}

Olse:
Datum a cas: {3}
Prutok [l/s]: {4}

------------------
Datum a cas kontroly: {5}
Soucet [l/s]: {6}
""".format(self.get_level_message(limit_type), date_lomna, flow_lomna, date_olse, flow_olse, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), flow_sum)

  def get_sms_message(self, flow_sum, limit_type):
    return 'Jablunkov - {0}, Soucet [l/s] = {1}'.format(self.get_level_message(limit_type), flow_sum)

  def get_level_message(self, limit_type):
    if limit_type == LimitType.LOW:
      return 'Nizky prutok - ODSTAVIT ELEKTRARNU'
    elif limit_type == LimitType.HIGH:
      return 'Dostacujici prutok - ZAPNOUT ELEKTRARNU'
    else:
      raise Exception('Error limit type value: {}'.format(limit_type))
    
