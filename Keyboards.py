from aiogram import types
clear_filt_shop_keyboard = types.InlineKeyboardMarkup()
shop_ikeyboard = types.InlineKeyboardMarkup()
type_filt_ikeyboard = types.InlineKeyboardMarkup()
track_ikeyboard = types.InlineKeyboardMarkup()


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
track_button = types.InlineKeyboardButton('Відстежувати', callback_data='track')



shop_ikeyboard.add(all_shop_button, cost_shop_button, type_shop_button, rarity_button, result_button)
clear_filt_shop_keyboard.add(clear_button)
track_ikeyboard.add(track_button)
type_filt_ikeyboard.add(clear_button, outfit_button, glider_button, pickaxe_button, emote_button, wrap_button, backpack_button, contrail_button, save_button)