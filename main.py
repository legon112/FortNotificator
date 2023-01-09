import asyncio
import logging

from FortFunc import all_shop, answerfiltshop, answer_type_shop, inline_rarity, all_rarity_dict, answer_rarity_shop, result_shop, searchfn, onstartup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from decouple import config

API_TOKEN = config('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    search = State()
    shop = State()
    shop_cost_filt = State()
    shop_type_filt = State()
    shop_rarity_filt = State()


main_keyboard = types.ReplyKeyboardMarkup()
shop_keyboard = types.ReplyKeyboardMarkup()
clear_filt_shop_keyboard = types.InlineKeyboardMarkup()
shop_ikeyboard = types.InlineKeyboardMarkup()
type_filt_ikeyboard = types.InlineKeyboardMarkup()

start_button = types.KeyboardButton('/start')
shop_button = types.KeyboardButton('/shop')
exit_button = types.KeyboardButton('/exit')
search_button  = types.KeyboardButton('/search')
clear_button = types.InlineKeyboardButton('Очистити фільтр', callback_data='clear')
notification_button = types.KeyboardButton('/notification')
all_shop_button = types.InlineKeyboardButton('Увесь магазин', callback_data='all')
cost_shop_button = types.InlineKeyboardButton('По ціні', callback_data='price')
type_shop_button = types.InlineKeyboardButton('По типу предмета', callback_data='type')
rarity_button = types.InlineKeyboardButton('По рідкості', callback_data="rarity")
outfit_button = types.InlineKeyboardButton('Hаряд', callback_data='outfit')
glider_button = types.InlineKeyboardButton('Дельтаплан', callback_data='glider')
pickaxe_button = types.InlineKeyboardButton('Кирка', callback_data='pickaxe')
emote_button = types.InlineKeyboardButton('Емоція', callback_data='emote')
wrap_button = types.InlineKeyboardButton('Обгортка', callback_data='wrap')
backpack_button = types.InlineKeyboardButton('Наплічник', callback_data='backpack')
contrail_button = types.InlineKeyboardButton('Слід', callback_data='contrail')
save_button = types.InlineKeyboardButton('Зберегти', callback_data='save')
result_button = types.InlineKeyboardButton('Результат', callback_data='result')


main_keyboard.add(start_button ,shop_button, search_button, notification_button)
shop_keyboard.add(exit_button)
shop_ikeyboard.add(all_shop_button, cost_shop_button, type_shop_button, rarity_button, result_button)
clear_filt_shop_keyboard.add(clear_button)
exit_keyboard = main_keyboard
exit_keyboard.add(exit_button)

type_filt_ikeyboard.add(clear_button, outfit_button, glider_button, pickaxe_button, emote_button, wrap_button, backpack_button, contrail_button, save_button)


filt_dict = {}
    

@dp.message_handler(commands=['start'], state = '*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Привіт, я бот для магазину фортнайт\nТут можешь знайти інформацію про різні предмети, актуальний магазин та можешь встановити сповіщення на наявність певних предметів\n/help - усі команди", reply_markup=main_keyboard)
    while True:
        onstartup()
        await asyncio.sleep(300)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply('/start - повернення на початок\n\
            /shop – перехід у стан магазину, в ньому можна отримати список усіх предметів у магазині з ціною(не дуже зручно, тому що кожен день у середньому в магазині ~90 предметів), можна виставляти фільтри по ціні.\
            /search – перехід у стан пошуку, в ньому користувач вводить назву предмета, а бот відправляє інформацію про предмет\
            /notification – перехід у стан сповіщення, в ньому можна написати назву предмета, потім, коли цей предмет з’явиться у магазині, прийде сповішення про його наявність.')


'''!!!SEARCH!!!'''
@dp.message_handler(commands=['search'], state = '*')
async def shop(message: types.Message, state: FSMContext):
    await Form.search.set()
    await message.answer('Введите точное название предмета\n/exit - выход:',reply_markup=exit_keyboard)

@dp.message_handler(commands=['exit'], state = Form.search)
async def shop(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы вышли из поиска предметов',reply_markup=main_keyboard)

@dp.message_handler(state = Form.search)
async def shop(message: types.Message, state: FSMContext):
    result = searchfn(message.text)
    if result['result']:
        ans_1 = 'name'
        ans_2 = 'value'
        ans_3 = 'series'
        ans_4 = 'description'
        await bot.send_photo(message.chat.id, result['image'], f'*{result.get(ans_1)}*\n\n*Редкость*: {result.get(ans_2)}\n*Серия*: {result.get(ans_3)}\n*Описание*: {result.get(ans_4)}', 'Markdown')
    else:
        await message.answer('Предмет не найден')
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
        await query.message.edit_text(answer_type_shop(filt_dict), reply_markup=type_filt_ikeyboard)
    elif query.data == 'rarity':   
        await Form.shop_rarity_filt.set()
        await query.message.edit_text(answer_rarity_shop(filt_dict), reply_markup=inline_rarity())
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
        await query.message.edit_text(answer_rarity_shop(filt_dict), reply_markup=inline_rarity())
        
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
        await query.message.edit_text(answer_type_shop(filt_dict), reply_markup=type_filt_ikeyboard)

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

@dp.message_handler()
async def echo(message: types.Message):
    pass
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)