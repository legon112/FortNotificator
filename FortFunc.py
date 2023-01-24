import datetime
import json
import requests

from aiogram import types
from decouple import config
from os.path import exists

API_TOKEN = config('FORT_API_TOKEN')


all_type_dict = {'glider' : 'Дельтоплан', 'outfit' : 'Наряд', 'wrap' : "Обгортка", 'backpack' : 'Наплічник', 'pickaxe' : "Кирка", 'emote' : 'Емоція', 'contrail' : 'Слід'}



all_all = {}
dict_all = {}
all_shopp = {}
all_rarity_dict = {}
all_list = []
update = True
notification_dict = {}
read_file = True
json_notification_file = 'notification.json'


def onstartup() -> bool:
    global read_file
    global all_all
    global dict_all 
    global all_shopp
    global all_rarity_dict
    global update
    global notification_dict
    categories = ['featured', 'daily']
    json_shop_file = 'combined.json'
    json_br_file = 'br.json'
    json_update_file = 'timeupdate.json'
    d1 = datetime.datetime.utcnow()
    time_update = datetime.datetime.utcnow()
    #Вытаскивание последней даты обновления
    try:
        with open(json_update_file, 'r+', encoding='utf-8') as f:
            data = f.read()
            time_update = json.loads(data)
        time_update = datetime.datetime(time_update[0], time_update[1], time_update[2])         
        d2 = [d1.year, d1.month, d1.day]
        with open(json_update_file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(d2))
    except:
        d2 = [d1.year, d1.month, d1.day]
        with open(json_update_file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(d2))
        
             
        #Вытаскивание информации про уведомления
    if read_file: 
        try:
            with open(json_notification_file, 'r+', encoding='utf-8') as f:
                data = f.read()
                notification_dict = json.loads(data)
        except:
            pass
            open(json_notification_file, "w")
        read_file = False
    
            
            
    #Проверка, обновился на то, обновился ли магазин; Обновление инфы
    if (d1-time_update).days >= 1 or not exists(json_br_file) or not exists(json_shop_file):
        all_shopp = requests.get(url='https://fortnite-api.com/v2/shop/br/combined?language=ru',headers= {'Authorization' : API_TOKEN}).json()
        with open(json_shop_file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(all_shopp))
        all_all = requests.get(url='https://fortnite-api.com/v2/cosmetics/br?language=ru',headers= {'Authorization' : API_TOKEN}).json()
        with open(json_br_file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(all_all))
        update = True
    else: 
        if not all_all or not all_shopp:
            with open(json_br_file, 'r', encoding='utf-8') as f:
                data = f.read()
                all_all = json.loads(data)        
            with open(json_shop_file, 'r', encoding='utf-8') as f:
                data = f.read()
                all_shopp = json.loads(data)
    #Обновление словаря с предметами из магазина   
    if update:
        for it in categories:
            for i in range(len(all_shopp["data"][it]['entries'])):
                item = all_shopp['data'][it]['entries'][i]
                if item['bundle']:
                    namee = item['bundle']['name']
                else:
                    namee = item['items'][0]['name']
                    all_rarity_dict.update({item['items'][0]['rarity']['value'] : item['items'][0]['rarity']['displayValue']})
                price = item['finalPrice']
                rarity = item['items'][0]['rarity']['value']
                typee = item['items'][0]['type']['value']
                dict_all.update({namee : {'price' : price, 'type' : typee, 'rarity' : rarity}})
                update = False
        #Рассылка
        for_people_dict = {}
        notif_list = list(notification_dict.keys())
        for i in notif_list:
            if i in dict_all.keys():
                for_people_dict[i] = notification_dict[i]               
                notification_dict.pop(i)
        with open(json_notification_file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(notification_dict))
        return [True, for_people_dict]
    return [False]

def notfic_ikeyboard(id):
    keyboard = types.InlineKeyboardMarkup()
    for i in notification_dict.keys():
        id_list = notification_dict[i]
        if id in id_list:
            keyboard.add(types.InlineKeyboardButton(i, callback_data=i))
    return keyboard

def del_notif(item : str, id):
    change = False  
    if id in notification_dict[item]:
        notification_dict[item].remove(id)
        change= True
    if not notification_dict[item]:
        notification_dict.pop(item)
        change = True
    if change:
        with open(json_notification_file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(notification_dict))

def track(item : str, id : str or int):
    global notification_dict
    item_names = list(notification_dict.keys())
    counter = False
    if not item in item_names:
        notification_dict[item] = [id]
        counter = True
    elif not id in notification_dict[item]:
        notification_dict[item].append(id)
        counter = True
    if counter:
        with open(json_notification_file, "w") as outfile:
            outfile.write(json.dumps(notification_dict))
    
    
    
    
def searchfn(item: str) -> dict:
    items = all_all['data']
    for i in range(len(items)):
        if items[i]['name'].lower() == item.lower():
            try:
                answer = {'result': True, 'name' : items[i]['name'], 'image' : items[i]['images']["featured"], 'value' : items[i]["rarity"]["displayValue"], 'series' : items[i]['set']['value'], 'description' : items[i]['description']}
            except:
                answer = {'result': True, 'name' : items[i]['name'], 'image' : items[i]['images']["icon"], 'value' : items[i]["rarity"]["displayValue"], 'series' : '-', 'description' : items[i]['description']}
            return answer
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

def inline_type(filt_dict : dict):
    all_type = {'outfit' : "Наряд", 'glider' : 'Дельтаплан', 'pickaxe' : 'Кирка', 'emote' : 'Емоція', 'wrap' : 'Обгортка', 'backpack' : 'Наплічник', 'contrail' : 'Слід'}
    type_ikeyboard = types.InlineKeyboardMarkup()
    type_ikeyboard.add(types.InlineKeyboardButton('Очистити фільтр', callback_data='clear'))
    if filt_dict and 'type' in filt_dict.keys():
        for i in all_type.keys():
            if i in filt_dict['type']:
                continue
            type_ikeyboard.add(types.InlineKeyboardButton(all_type[i], callback_data=i))
        type_ikeyboard.add(types.InlineKeyboardButton('Зберегти', callback_data='save'))
    else:
        for i in all_type.keys():
            type_ikeyboard.add(types.InlineKeyboardButton(all_type[i], callback_data=i))
        type_ikeyboard.add(types.InlineKeyboardButton('Зберегти', callback_data='save'))
    return type_ikeyboard

def inline_rarity(filt_dict : dict):
    rarity_ikeyboard = types.InlineKeyboardMarkup()
    
    rarity_ikeyboard.add(types.InlineKeyboardButton('Очистити фільтр', callback_data='clear'))
    if filt_dict and 'rarity' in filt_dict.keys():
        for i in all_rarity_dict.keys():
            if i in filt_dict['rarity']:
                continue
            rarity_ikeyboard.add(types.InlineKeyboardButton(all_rarity_dict[i], callback_data=i))
        rarity_ikeyboard.add(types.InlineKeyboardButton('Зберегти', callback_data='save'))
    else:
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