import json
import requests
from aiogram import types

from decouple import config

API_TOKEN = config('FORT_API_TOKEN')


all_type_dict = {'glider' : 'Дельтоплан', 'outfit' : 'Наряд', 'wrap' : "Обгортка", 'backpack' : 'Наплічник', 'pickaxe' : "Кирка", 'emote' : 'Емоція', 'contrail' : 'Слід'}
# b = requests.get(url='https://fortnite-api.com/v2/shop/br/combined?language=ru',headers= {'Authorization' : API_TOKEN}).json()
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
    dict_all.update({namee : price})
    
def all_shop() -> str:
    global all_list
    all_keys = tuple(dict_all.keys())
    if not all_list:
        for i in all_keys:
            all_list.append(f'{i} : {dict_all[i]}')           
    return '\n'.join(all_list)

def answerfiltshop(filt = {}) -> str:
    answers_list = []
    keys = filt.keys()
    if filt:
        answers_list.append('Поточні фільтри:')   
        all_filt_dict = {'cost': 'Ціна', 'type' : 'Тип'}
        itt = 0
        for i in filt.keys():
            if i == 'cost':
                answers_list.append('\n' + all_filt_dict[i] + ' : ')
                for it in range(len(filt[i])):
                    if not itt:
                        answers_list.append(str(filt[i][it]))
                        itt += 1
                    else:
                        answers_list.append('-' + str(filt[i][it]))
            elif i == 'type':
                answers_list.append('\n' + all_filt_dict[i] + ' : ' + ', '.join(all_type_dict[i].lower() for i in filt[i]))
        answers_list.append('\nСкид фільра у меню фільра')
    answers_list.append('\nЯкі фільтри ви хочете застосувати:')
    return ''.join(answers_list)


def answer_type_shop(filt = {}) -> str:
    answers_list = []
    if 'type' in filt.keys():
        filt_message = '\n'.join(all_type_dict[i] for i in filt['type'])
        answers_list.append(f'Поточні фільтри:\n{filt_message}')
    answers_list.append('\nОберіть які типи предметів вас цікавять:')
    return ''.join(answers_list)
        

def inlineshop():
    pass


def test(fa = '123'):
    print(fa)
    return









