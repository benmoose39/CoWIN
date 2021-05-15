print(r'''
  ____   __        _____ _   _       _  __              _
 / ___|__\ \      / /_ _| \ | |     | |/ /___ _ __ __ _| | __ _
| |   / _ \ \ /\ / / | ||  \| |_____| ' // _ \ '__/ _` | |/ _` |
| |__| (_) \ V  V /  | || |\  |_____| . \  __/ | | (_| | | (_| |
 \____\___/ \_/\_/  |___|_| \_|     |_|\_\___|_|  \__,_|_|\__,_|

''')

import os
import sys
yes = ['y', 'Y']
while(True):
        try:
            print('Checking dependecies... ',end='')
            import requests
            import json
            import datetime
            import webbrowser
            print(f"[OK]")
            break
        except ModuleNotFoundError as nomodule:
            print(f"\n[!] {nomodule}")
            module = str(nomodule)[17:-1]
            if input(f"[?] Attempt to install {module}?(y/N) ") in yes:
                if os.system(f"pip install {module}") == 0:
                    continue
            print(f"[!] Unable to install {module}. Try manually and come back")


headers = {
    'authority': 'cdn-api.co-vin.in',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-gpc': '1',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9'
#    'if-none-match': 'W/"2b9-sbQ2jbudzJKWfKTRIx+h9YBRmWE"',
}

kerala = {
    'Alappuzha': 301,
    'Ernakulam': 307,
    'Idukki': 306,
    'Kannur': 297,
    'Kasaragod': 295,
    'Kollam': 298,
    'Kottayam': 304,
    'Kozhikode': 305,
    'Malappuram': 302,
    'Palakkad': 308,
    'Pathanamthitta': 300,
    'Thiruvananthapuram': 296,
    'Thrissur': 303,
    'Wayanad': 299
    }

district = input('Enter district: ').title()
if district not in kerala:
    print('No such district in Kerala')
    sys.exit()

district_code = kerala[district]

result = {
    'Center_ID':[],
    'Name':[],
    'Address':[],
    'Fee':[],
    'Sessions':[]
    }

days = 7
duplicate_check = ''
for i in range(days):
    date = (datetime.date.today() + datetime.timedelta(days=i))
    date = date.strftime("%d-%m-%Y")
    
    response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_code}&date={date}', headers=headers)
    centers = response.json()['centers']

    if response.text == duplicate_check:
        continue
    duplicate_check = response.text
    
    if i == days-1 and not result['Center_ID']:
        sys.exit()
    else:
        for item in centers:
            result['Center_ID'].append(item['center_id'])
            result['Name'].append(item['name'])
            result['Address'].append(f"{item['address']}, {item['pincode']}")
            result['Fee'].append(item['fee_type'])
            result['Sessions'].append(item['sessions'])
            
filename = f"{district}_CoWIN.txt"

with open(f'{filename}', 'w') as f:
    for i in range(len(result['Name'])):
        #print()
        f.write('\n')
        for item in result:
            if item != 'Sessions':
                #print(f"{item} : {result[item][i]}")
                f.write(f"{item} : {result[item][i]}\n")
            else:
                for session in result[item][i]:
                    for thing in ['date', 'vaccine', 'min_age_limit', 'slots']:
                        #print(f"{thing} : {session[thing]}")
                        f.write(f"{thing} : {session[thing]}\n")
        f.write('-' * 200)

url = f"file://{os.path.realpath(filename)}".replace(' ','%20').replace('\\','/')
#print(url)
os.system(f"start chrome {url}")
#webbrowser.open(url)
