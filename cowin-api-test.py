print(r'''
  ____   __        _____ _   _     ____  _
 / ___|__\ \      / /_ _| \ | |   |  _ \| | ___  __ _ ___  ___
| |   / _ \ \ /\ / / | ||  \| |   | |_) | |/ _ \/ _` / __|/ _ \
| |__| (_) \ V  V /  | || |\  |   |  __/| |  __/ (_| \__ \  __/_ _ _
 \____\___/ \_/\_/  |___|_| \_|___|_|   |_|\___|\__,_|___/\___(_|_|_)
                             |_____|

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
            print(f"[OK]")
            break
        except ModuleNotFoundError as nomodule:
            print(f"\n[!] {nomodule}")
            module = str(nomodule)[17:-1]
            if input(f"[?] Attempt to install {module}?(y/N) ") in yes:
                if os.system(f"pip install {module}") == 0:
                    continue
            print(f"[!] Unable to install {module}. Try manually and come back")

#import pandas as pd

headers = {
    'authority': 'cdn-api.co-vin.in',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-gpc': '1',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    'if-none-match': 'W/"5d8-2jrF3Zf1hjCMuSob9rLD7lhEGJI"',
}

kerala = {295: 'Kasaragod', 296: 'Thiruvananthapuram', 298: 'Kollam', 299: 'Wayanad', 300: 'Pathanamthitta', 301: 'Alappuzha', 302: 'Malappuram', 303: 'Thrissur', 305: 'Kozhikode', 306: 'Idukki', 307: 'Ernakulam', 297: 'Kannur', 304: 'Kottayam', 308: 'Palakkad'}

district = input('Enter district: ')
if district.title() not in kerala.values():
    print('No such district in Kerala')
    sys.exit()
    
for key in kerala:
    if kerala[key] == district.title():
        id = key

result = {'DATE':[],
                  'Center_ID':[],
                  'Name':[],
                  'Vaccine':[],
                  'from':[],
                  'to':[],
                  'Capacity':[],
                  'Fee':[],
                  'Slots':[]}

days = 7
for i in range(days):
    date = (datetime.date.today() + datetime.timedelta(days=i))
    date = date.strftime("%d-%m-%Y")
    
    response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={id}&date={date}', headers=headers)

    appointment = json.loads(response.text)
    #print(date)
    #print(appointment)
    if appointment['sessions'] == []:
        print(f"No slots on {date}")
        if i == days-1 and not result['DATE']:
            sys.exit()
    else:
        for item in appointment['sessions']:
            result['DATE'].append(item['date'])
            result['Center_ID'].append(item['center_id'])
            result['Name'].append(f"{item['name']}, {item['block_name']}, PIN:{item['pincode']}")
            result['Vaccine'].append(item['vaccine'])
            result['from'].append(item['from'])
            result['to'].append(item['to'])
            result['Capacity'].append(item['available_capacity'])
            result['Fee'].append(item['fee_type'])
            result['Slots'].append(item['slots'])

#slots = pd.DataFrame(result)
for i in range(len(result['Name'])):
    print()
    for item in result:
        print(f"{item} : {result[item][i]}")
    print()


