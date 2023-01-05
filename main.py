import logging

from FortFunc import all_shop
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
    shop = State()



main_keyboard = types.ReplyKeyboardMarkup()
shop_keyboard = types.ReplyKeyboardMarkup()
shop_ikeyboard = types.InlineKeyboardMarkup()

shop_button = types.KeyboardButton('/shop')
exit_button = types.KeyboardButton('/exit')
search_button  = types.KeyboardButton('/search')
notification_button = types.KeyboardButton('/notification')
all_shop_button = types.InlineKeyboardButton('Увесь магазин', callback_data='all')
cost_shop_button = types.InlineKeyboardButton('По ціні', callback_data='cost')
type_shop_button = types.InlineKeyboardButton('По типу предмета', callback_data='cost')


main_keyboard.add(shop_button, search_button, notification_button)
shop_keyboard.add(exit_button)
shop_ikeyboard.add(all_shop_button, cost_shop_button, type_shop_button)


@dp.message_handler(commands=['start'], state = '*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Привіт, я бот для магазину фортнайт\nТут можешь знайти інформацію про різні предмети, актуальний магазин та можешь встановити сповіщення на наявність певних предметів\n/help - усі команди", reply_markup=main_keyboard)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply('/start - повернення на початок\n\
            /shop – перехід у стан магазину, в ньому можна отримати список усіх предметів у магазині з ціною(не дуже зручно, тому що кожен день у середньому в магазині ~90 предметів), можна виставляти фільтри по ціні.\
            /search – перехід у стан пошуку, в ньому користувач вводить назву предмета, а бот відправляє інформацію про предмет\
            /notification – перехід у стан сповіщення, в ньому можна написати назву предмета, потім, коли цей предмет з’явиться у магазині, прийде сповішення про його наявність.')



@dp.message_handler(commands=['shop'])
async def shop(message: types.Message, state: FSMContext):
    await Form.shop.set()
    await message.answer('Які фільтри ви хочете застосувати:', reply_markup= shop_ikeyboard)

@dp.callback_query_handler(state=Form.shop)
async def value_query(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'all':
        await query.message.edit_text(all_shop())
    
    



@dp.message_handler()
async def echo(message: types.Message):
    pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)