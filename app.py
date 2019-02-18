from bs4 import BeautifulSoup
import requests

headers = {
    'Cookie': 'easyid-identity=1LOvBJh2et5Y0B45dshbSljVlIQTmhueI_BwFPi9SkYW8OoBHHM0cqKBs7HkDMJNxAQeUNufhMc64lmXglmTtUTZFBtUbizGX1EvHTBXAQOW2QaKs4KpMvWkUeA8qRXLie5u2mUwihbiXrNP2SqXD87aUCQ3LyHUweleEft0YnVVzjaFHIjyY2_1fNzkZqgqyiFR8sqsER9y_Oyh8MJdYArHE4DE2hvJoHA1poziH0im97X4FTT_4uSEIiDQgasy3tRANdeZGKWLHr0fOUAXu0fQu0gIx7_xH9eSkFgUHyfAaMnS0NKXEuW_zRWhp08Bkf_kslsGg84xbIb2q5wVbWsXnLYIj5E0m4MVmTpUDqR1wPwAZ18lcrkIxaCNfDNhAgse5CWtTfvlqMHkXGJghjuXdS9JuAYoiyH_vX9FWs9RIzKUOaLqWkII5BjoVi8LuSog6BYdOfXp3h9KmMCgAJUSMWfjh2Iyg0tNWj3kVoAffg4nqcOQTKyCpRu5GBscFu9vYEPH1ySIBaTZ8lWhEu1PhMKnOJLel-910D7mHfbWOi1Bj0udn7IvYrxPsp_LhZrcfF6hS9wLHPxTKiQI3Nw; ischmihpps=keb8vhhqnjiiacge57lg1hm4f3',
    'cache-control': 'no-cache',
    'Postman-Token': 'd2f267a3-8479-4a78-a2bc-ca6813909f4d'
    }
print('headers')

content = requests.request('GET', 'http://hydro.chmi.cz', headers=headers)
print('test')

#with requests.Session() as s:

#  content = s.get('http://hydro.chmi.cz', headers=headers)
#  print(content)

print('test 2')
soup = BeautifulSoup(content, 'html.parser')

print(soup.prettify())