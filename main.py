import asyncio
import logging

from FortFunc import all_shop, answerfiltshop, answer_type_shop, inline_rarity, all_rarity_dict, answer_rarity_shop, result_shop, searchfn, onstartup, track, notfic_ikeyboard, del_notif, inline_type
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from decouple import config
from Keyboards import shop_ikeyboard, clear_filt_shop_keyboard, track_ikeyboard, type_filt_ikeyboard

API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    search = State()
    notnotification = State()
    shop = State()
    shop_cost_filt = State()
    shop_type_filt = State()
    shop_rarity_filt = State()



filt_dict = {}
notification_answer = '*Управління сповіщеннями*\nДля видалення предмету зі списку сповіщень, натисніть на назву предмата:'

async def start():
    while True:
            answer = onstartup()
            if answer[0]:            
                items = answer[1]
                for i in items.keys():
                    for it in items[i]:
                        await bot.send_message(it,f'Хей, {i} зараз у магазині! Нумо його купувати)')        
            await asyncio.sleep(300)

@dp.message_handler(commands=['start'], state = '*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Привіт, я бот для магазину фортнайт\nТут можешь знайти інформацію про різні предмети, актуальний магазин та можешь встановити сповіщення на наявність певних предметів\n/help - усі команди", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply('/start - повернення на початок\n/shop – перехід у стан магазину, в ньому можна отримати список усіх предметів у магазині з ціною(не дуже зручно, тому що кожен день у середньому в магазині ~90 предметів), можна виставляти фільтри по ціні.\n/search – перехід у стан пошуку, в ньому користувач вводить назву предмета, а бот відправляє інформацію про предмет, завдяки кнопці "Відстежувати" предмет можна додати у список сповіщень\n/notification – перехід у стан сповіщення, контроль предметів у списку сповіщень')



'''!!!notification!!!'''
@dp.message_handler(commands=['notification'], state = '*')
async def shop(message: types.Message, state: FSMContext):
    await Form.notnotification.set()
    await message.answer(notification_answer, 'Markdown', reply_markup=notfic_ikeyboard(message.chat.id))

@dp.callback_query_handler(state=Form.notnotification)
async def value_query(query: types.CallbackQuery, state: FSMContext):
    try:
        del_notif(query.data, query.message.chat.id)
        await query.message.edit_text(notification_answer, 'Markdown', reply_markup=notfic_ikeyboard(query.message.chat.id))
    except:
        await query.message.answer('Якщо ви заблукали напишіть /help')
    


'''!!!SEARCH!!!'''
@dp.message_handler(commands=['search'], state = '*')
async def shop(message: types.Message, state: FSMContext):
    await Form.search.set()
    await message.answer('Введите точное название предмета\n/exit - выход:')

@dp.message_handler(commands=['exit'], state = Form.search)
async def shop(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы вышли из поиска предметов')

@dp.message_handler(state = Form.search)
async def shop(message: types.Message, state: FSMContext):
    result = searchfn(message.text)
    if result['result']:
        ans_1 = 'name'
        ans_2 = 'value'
        ans_3 = 'series'
        ans_4 = 'description'
        async with state.proxy() as data:
            data['track'] = result[ans_1]
        await bot.send_photo(message.chat.id, result['image'], f'*{result.get(ans_1)}*\n\n*Редкость*: {result.get(ans_2)}\n*Серия*: {result.get(ans_3)}\n*Описание*: {result.get(ans_4)}', 'Markdown', reply_markup=track_ikeyboard)
    else:
        await message.answer('Предмет не найден')
        
@dp.callback_query_handler(state=Form.search)
async def value_query(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'track':
        async with state.proxy() as data:   
            item = data['track']
        track(item, query.message.chat.id)
        await query.message.answer(f'{item} тепер відстежуеється')
'''!!!END  SEARCH!!!'''


"""!!!SHOP!!!"""
@dp.message_handler(commands=['shop'], state = '*')
async def shop(message: types.Message, state: FSMContext):
    filt_dict.clear()
    await Form.shop.set()
    await message.answer(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard)
    
@dp.callback_query_handler(state=Form.shop)
async def value_query(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'all':
        await state.finish()
        await query.message.edit_text(all_shop())      
    elif query.data == 'price':
        await Form.shop_cost_filt.set()
        await query.message.edit_text('Введить ціну(1500) або від та до(1000-1500) якої ціни предмети вас цікавлять, clear - скидання фільтра', reply_markup=clear_filt_shop_keyboard)
    elif query.data == 'type':
        await Form.shop_type_filt.set()
        await query.message.edit_text(answer_type_shop(filt_dict), reply_markup=inline_type(filt_dict))
    elif query.data == 'rarity':   
        await Form.shop_rarity_filt.set()
        await query.message.edit_text(answer_rarity_shop(filt_dict), reply_markup=inline_rarity(filt_dict))
    elif query.data == 'result':
        await state.finish()
        await query.message.edit_text(result_shop(filt_dict))
              
@dp.callback_query_handler(state=Form.shop_rarity_filt)
async def type_query(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'clear':        
        if 'rarity' in filt_dict.keys():
            filt_dict.pop('rarity')
        await Form.shop.set()
        await query.message.edit_text(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard)
    elif query.data == 'save':
        await Form.shop.set()
        await query.message.edit_text(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard) 
    elif query.data in all_rarity_dict.keys():
        if 'rarity' in filt_dict.keys():
            filt_dict['rarity'].add(query.data)
        else:
            filt_dict['rarity'] = {query.data}
        await query.message.edit_text(answer_rarity_shop(filt_dict), reply_markup=inline_rarity(filt_dict))
        
@dp.callback_query_handler(state=Form.shop_type_filt)
async def type_query(query: types.CallbackQuery, state: FSMContext):
    all_type = ('glider', 'outfit', 'wrap', 'backpack', 'pickaxe', 'emote', 'contrail')
    if query.data == 'clear':        
        if 'type' in filt_dict.keys():
            filt_dict.pop('type')
        await Form.shop.set()
        await query.message.edit_text(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard)
    elif query.data == 'save':
        await Form.shop.set()
        await query.message.edit_text(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard) 
    elif query.data in all_type:
        if 'type' in filt_dict.keys():
            filt_dict['type'].add(query.data)
        else:
            filt_dict['type'] = {query.data}
        await query.message.edit_text(answer_type_shop(filt_dict), reply_markup=inline_type(filt_dict))

@dp.callback_query_handler(state=Form.shop_cost_filt)
async def cost_query(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'clear':        
        if 'price' in filt_dict.keys():
            filt_dict.pop('price')
        await Form.shop.set()
        await query.message.edit_text(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard)

@dp.message_handler(state=Form.shop_cost_filt)
async def cost_filt_shop(message: types.Message, state: FSMContext):
    filt_message = message.text.replace('-', ' ')
    filt_list = [int(i) for i in filt_message.split()]
    if filt_message.replace(' ','').isdigit() and len(filt_list) <= 2:        
        filt_list = sorted(filt_list)
        filt_dict.update({'price' : filt_list})
    await Form.shop.set()
    await message.answer(answerfiltshop(filt_dict), reply_markup= shop_ikeyboard)
"""!!!END SHOP!!!"""   

@dp.message_handler(state='*')
async def echo(message: types.Message):
    await message.answer('Якщо ви заблукали напишіть /help')
    
@dp.callback_query_handler(state='*')
async def echo(message: types.Message):
    await message.answer('Якщо ви заблукали напишіть /help')
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    executor.start_polling(dp, skip_updates=True)