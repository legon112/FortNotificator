import json
import requests

from decouple import config

API_TOKEN = config('FORT_API_TOKEN')

# b = requests.get(url='https://fortnite-api.com/v2/shop/br/combined',headers= {'Authorization' : API_TOKEN}).json()
with open('combinen.json', 'r', encoding='utf-8') as f:
    data = f.read()
    b = json.loads(data)
dict_all = {}
all_list = []
for i in range(len(b['data']['featured']['entries'])):
    item = b['data']['featured']['entries'][i]
    if item['bundle']:
        namee = item['bundle']['name']
    else:
        namee = item['items'][0]['name']
    price = item['finalPrice']
    # print(namee)
    
    dict_all.update({namee : price})
    
def all_shop():
    global all_list
    all_keys = tuple(dict_all.keys())
    if not all_list:
        for i in all_keys:
            all_list.append(f'{i} : {dict_all[i]}')           
    return '\n'.join(all_list)