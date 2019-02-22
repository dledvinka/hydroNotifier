from bs4 import BeautifulSoup
import requests
import logging

class DataScrapper:

  data_sources = {
    'Lomna': 'http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307326',
    'Olse': 'http://hydro.chmi.cz/hpps/popup_hpps_prfdyn.php?seq=307325'
  }

  headers = {
    # 'Cookie': 'easyid-identity=1LOvBJh2et5Y0B45dshbSljVlIQTmhueI_BwFPi9SkYW8OoBHHM0cqKBs7HkDMJNxAQeUNufhMc64lmXglmTtUTZFBtUbizGX1EvHTBXAQOW2QaKs4KpMvWkUeA8qRXLie5u2mUwihbiXrNP2SqXD87aUCQ3LyHUweleEft0YnVVzjaFHIjyY2_1fNzkZqgqyiFR8sqsER9y_Oyh8MJdYArHE4DE2hvJoHA1poziH0im97X4FTT_4uSEIiDQgasy3tRANdeZGKWLHr0fOUAXu0fQu0gIx7_xH9eSkFgUHyfAaMnS0NKXEuW_zRWhp08Bkf_kslsGg84xbIb2q5wVbWsXnLYIj5E0m4MVmTpUDqR1wPwAZ18lcrkIxaCNfDNhAgse5CWtTfvlqMHkXGJghjuXdS9JuAYoiyH_vX9FWs9RIzKUOaLqWkII5BjoVi8LuSog6BYdOfXp3h9KmMCgAJUSMWfjh2Iyg0tNWj3kVoAffg4nqcOQTKyCpRu5GBscFu9vYEPH1ySIBaTZ8lWhEu1PhMKnOJLel-910D7mHfbWOi1Bj0udn7IvYrxPsp_LhZrcfF6hS9wLHPxTKiQI3Nw; ischmihpps=keb8vhhqnjiiacge57lg1hm4f3',
    # 'cache-control': 'no-cache',
    # 'Postman-Token': 'd2f267a3-8479-4a78-a2bc-ca6813909f4d'
  }

  def __init__(self):
    pass


  def get_values(self):
    result = {}

    try:
      for key, url in self.data_sources.items():
        page_content = requests.request('GET', url, headers=self.headers)
        (date, flowLitresPerSecond) = self.get_current_value(page_content)
        result[key] = (date, flowLitresPerSecond)
    except Exception as e:
      logging.exception(e)

    return result


  def get_current_value(self, html_content):
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
