import json
import requests

from aiogram import types
from decouple import config
from sys import getsizeof

API_TOKEN = config('FORT_API_TOKEN')


all_type_dict = {'glider' : 'Дельтоплан', 'outfit' : 'Наряд', 'wrap' : "Обгортка", 'backpack' : 'Наплічник', 'pickaxe' : "Кирка", 'emote' : 'Емоція', 'contrail' : 'Слід'}

with open('br.json', 'r', encoding='utf-8') as f:
    all_all = json.loads(f.read())
# b = requests.get(url='https://fortnite-api.com/v2/shop/br/combined?language=ru',headers= {'Authorization' : API_TOKEN}).json()
with open('combinen.json', 'r', encoding='utf-8') as f:
    data = f.read()
    b = json.loads(data)
dict_all = {}
all_rarity_dict = {}
all_list = []
for i in range(len(b['data']['featured']['entries'])):
    item = b['data']['featured']['entries'][i]
    if item['bundle']:
        namee = item['bundle']['name']
    else:
        namee = item['items'][0]['name']
        all_rarity_dict.update({item['items'][0]['rarity']['value'] : item['items'][0]['rarity']['displayValue']})
    price = item['finalPrice']
    rarity = item['items'][0]['rarity']['value']
    typee = item['items'][0]['type']['value']
    dict_all.update({namee : {'price' : price, 'type' : typee, 'rarity' : rarity}})
    
    
def searchfn(item: str) -> dict:
    items = all_all['data']
    for i in range(len(items)):
        if items[i]['name'].lower() == item.lower():
            return {'result': True, 'name' : items[i]['name'], 'image' : items[i]['images']["featured"], 'value' : items[i]["rarity"]["displayValue"], 'series' : items[i]['set']['value'], 'description' : items[i]['description']}
    return {'result' : False}
    
def result_shop(filt : dict) -> str:
    answer = []
    if filt:
        for i in dict_all.keys():
            counter = False
            counter_2 = False
            for it in filt.keys():
                item = dict_all[i][it]
                filter = filt[it]
                if it == 'price':
                    if len(filter) == 2:
                        if item >= filter[0] and item <= filter[1]:
                            pass
                        else:
                            counter = True        
                    else:
                        if item == filter[0]:
                            pass
                        else:
                            counter = True                                       
                else:
                    if not item in filter:
                        counter = True
                if counter:
                    counter_2 = False
                    break
                counter_2 = True
            if counter_2:         
                price = str(dict_all[i]['price'])
                answer.append(f'{i} : {price}')
                
                     
        if not answer:
            answer.append('Нічого не знайшлось')
    else:
        answer.append('Фільтри не були застосовані(')
    return '\n'.join(answer)
    
def answer_rarity_shop(filt : dict) -> str:
    answers_list = []
    if 'rarity' in filt.keys():
        filt_message = '\n'.join(all_rarity_dict[i] for i in filt['rarity'])
        answers_list.append(f'Поточні фільтри:\n{filt_message}')
    answers_list.append('\nОберіть яка рідкість предметів вас цікавять:')
    return ''.join(answers_list) 
    
def inline_rarity():
    rarity_ikeyboard = types.InlineKeyboardMarkup()
    
    rarity_ikeyboard.add(types.InlineKeyboardButton('Очистити фільтр', callback_data='clear')) 
    # rarity_ikeyboard.add
    for i in all_rarity_dict.keys():
        rarity_ikeyboard.add(types.InlineKeyboardButton(all_rarity_dict[i], callback_data=i))
    rarity_ikeyboard.add(types.InlineKeyboardButton('Зберегти', callback_data='save'))
    return rarity_ikeyboard
    
    
def all_shop() -> str:
    global all_list
    all_keys = tuple(dict_all.keys())
    if not all_list:
        for i in all_keys:
            price = str(dict_all[i]['price'])
            all_list.append(f'{i} : {price}')           
    return '\n'.join(all_list)

def answerfiltshop(filt : dict) -> str:    
    answers_list = []
    if filt:
        answers_list.append('Поточні фільтри:')   
        all_filt_dict = {'price': 'Ціна', 'type' : 'Тип', 'rarity' : 'Рідкість'}
        itt = 0
        for i in filt.keys():
            if i == 'price':
                answers_list.append('\n' + all_filt_dict[i] + ' : ')
                for it in range(len(filt[i])):
                    if not itt:
                        answers_list.append(str(filt[i][it]))
                        itt += 1
                    else:
                        answers_list.append('-' + str(filt[i][it]))
            elif i == 'type':
                answers_list.append('\n' + all_filt_dict[i] + ' : ' + ', '.join(all_type_dict[i].lower() for i in filt[i]))
            elif i == 'rarity':
                answers_list.append('\n' + all_filt_dict[i] + ' : ' + ', '.join(all_rarity_dict[i] for i in filt[i]))
        answers_list.append('\nСкид фільтра у меню фільтра')
    answers_list.append('\nЯкі фільтри ви хочете застосувати:')
    return ''.join(answers_list)


def answer_type_shop(filt : dict) -> str:
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









