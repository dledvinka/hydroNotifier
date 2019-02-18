from bs4 import BeautifulSoup
import requests
import time
from timeloop import Timeloop
from datetime import timedelta
import datetime

limit_low_signalled = False
limit_high_signalled = True

headers = {
    'Cookie': 'easyid-identity=1LOvBJh2et5Y0B45dshbSljVlIQTmhueI_BwFPi9SkYW8OoBHHM0cqKBs7HkDMJNxAQeUNufhMc64lmXglmTtUTZFBtUbizGX1EvHTBXAQOW2QaKs4KpMvWkUeA8qRXLie5u2mUwihbiXrNP2SqXD87aUCQ3LyHUweleEft0YnVVzjaFHIjyY2_1fNzkZqgqyiFR8sqsER9y_Oyh8MJdYArHE4DE2hvJoHA1poziH0im97X4FTT_4uSEIiDQgasy3tRANdeZGKWLHr0fOUAXu0fQu0gIx7_xH9eSkFgUHyfAaMnS0NKXEuW_zRWhp08Bkf_kslsGg84xbIb2q5wVbWsXnLYIj5E0m4MVmTpUDqR1wPwAZ18lcrkIxaCNfDNhAgse5CWtTfvlqMHkXGJghjuXdS9JuAYoiyH_vX9FWs9RIzKUOaLqWkII5BjoVi8LuSog6BYdOfXp3h9KmMCgAJUSMWfjh2Iyg0tNWj3kVoAffg4nqcOQTKyCpRu5GBscFu9vYEPH1ySIBaTZ8lWhEu1PhMKnOJLel-910D7mHfbWOi1Bj0udn7IvYrxPsp_LhZrcfF6hS9wLHPxTKiQI3Nw; ischmihpps=keb8vhhqnjiiacge57lg1hm4f3',
    'cache-control': 'no-cache',
    'Postman-Token': 'd2f267a3-8479-4a78-a2bc-ca6813909f4d'
    }
#print('headers')

tl = Timeloop()

def get_current_value(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')

  big_table = soup.find('table', class_='stdstationtbl')
  third_table = big_table.find_all('tr', recursive=False)[2]
  rows = third_table.find_all('tr')

  for row in rows[1:]: 
    values = row.find_all('td')
    date = values[0].text
    stateCentiMeters = values[1].text
    flowLitresPerSecond = float(values[2].text) * 1000
    temperatureDegreeCelsius = values[3].text
    #print(flowLitresPerSecond)
    return date, flowLitresPerSecond

@tl.job(interval=timedelta(seconds=10))
def main_job():
  #content = requests.request('GET', 'http://hydro.chmi.cz', headers=headers)
  # Lomná
  content1 = requests.request('GET', 'http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307326')
  # Olše 
  content2 = requests.request('GET', 'http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307325')

  (date1, flow1) = get_current_value(content1.text)
  (date2, flow2) = get_current_value(content2.text)
  flow_sum = flow1 + flow2

  print(datetime.datetime.now())
  print(date1)
  print(flow_sum)
  # print(date2)
  # print(flow1)

  #Davide Olše + Lomňanka (součet) při poklesu pod 630 l/s pošle upozornění, že je málo vody - MVE se musí odstavit     
  #a při 650 l/s pošle, že je dost vody MVE může opět najet.

if __name__ == "__main__":
    tl.start(block=True)