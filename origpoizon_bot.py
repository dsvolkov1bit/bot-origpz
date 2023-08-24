import telebot
from telebot import types
import requests
import xml.dom.minidom as MD


# Ввод данных по стоимости доставки и страховки
delivery_china = 950        # Доставка по Китаю
delivery_moscow = 950       # Доставка до Москвы
commission = 900            # Комиссия

# Ссылка с инструкцией
link_ins = 'https://telegra.ph/Instrukciya-08-15-9'


id_admin = 140181967 # Идентификатор админа (туда будут отправляться заказы)

token='6626434237:AAEIGol_ZTOWino6mBraZfeFbml75SFKma4'



username = dict()
name = dict()
phone = dict()
link = dict()
size = dict()
delivery = dict()
x = dict()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🔐 Получить инструкцию')
    item2 = types.KeyboardButton('💵 Рассчитать стоимость')
    item3 = types.KeyboardButton('🔥 Оформить заказ')
    
    markup.add(item1, item2, item3)
    
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}! Мы выкупаем товары с Китайского маркетплейса Poizon и осуществляем их доставку в РФ. Благодаря данному боту вы сможете легко и быстро рассчитать стоимость и оформить заказ'.format(message.from_user))
    bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)

    
@bot.message_handler(content_types=['text'])
def bot_message(message):
    
    if message.chat.type =='private':
        
        if message.text == '🔐 Получить инструкцию':
        
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔐 Получить инструкцию')
            item2 = types.KeyboardButton('💵 Рассчитать стоимость')
            item3 = types.KeyboardButton('🔥 Оформить заказ')
            markup.add(item1, item2, item3)
            
            bot.send_message(message.chat.id, f'Обязательно прочитайте данную инструкцию перед оформлением заказа❗️ {link_ins} '.format(message.from_user))
            bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
        
        elif message.text == '💵 Рассчитать стоимость':
            
            delete = telebot.types.ReplyKeyboardRemove()
                       
            message_cost = bot.send_message(message.chat.id, 'Введите стоимость товара в Юанях и я посчитаю общую стоимость с доставкой в рублях:'.format(message.from_user), reply_markup = delete)

            bot.register_next_step_handler(message_cost,bot_message_cost)
               
        elif message.text == '🔥 Оформить заказ':
            
            cancel = types.ReplyKeyboardMarkup(resize_keyboard = True)
            back1 = types.KeyboardButton('🔴 Начать заново')
            cancel.add(back1)
                       
            message_name = bot.send_message(message.chat.id, 'Введите свои данные. Фамилия Имя:'.format(message.from_user), reply_markup = cancel)
            
            bot.register_next_step_handler(message_name,bot_message_name)

        elif message.text == '🔴 Начать заново':
        
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔐 Получить инструкцию')
            item2 = types.KeyboardButton('💵 Рассчитать стоимость')
            item3 = types.KeyboardButton('🔥 Оформить заказ')
            markup.add(item1, item2, item3)
            
            bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)


def bot_message_cost(message):
    
    try:
        
        # Парсинг курса Юаня с гугла
        uan_url = 'https://www.cbr-xml-daily.ru/daily_utf8.xml'

        full_page = requests.get(uan_url).text

        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)


        xmlparse = MD.parseString(full_page)

        Valutes = xmlparse.getElementsByTagName("Valute")

        for valute in Valutes:
           
            CharCode = valute.getElementsByTagName("CharCode")[0]
            Value = valute.getElementsByTagName("Value")[0]
            CharCode = getText(CharCode.childNodes)
            Value = getText(Value.childNodes)
            if CharCode=='CNY':
                uan = round(float(Value.replace(',','.')),2) + 1
                continue
    
    
        markup_cost = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back1 = types.KeyboardButton('🔴 Начать заново')
        markup_cost.add(back1)
        
        x[message.from_user.id] = float(message.text.replace(',','.')) * uan + (delivery_china+delivery_moscow+commission)
        
        bot.send_message(message.chat.id, f"""Итоговая стоимость:

Актуальный курс юаня - {uan} руб.
Доставка по Китаю: {delivery_china} руб.
Доставка до Москвы: {delivery_moscow} руб.
Комиссия за услуги: {commission} руб.

Итого:
{message.text.replace(',','.')}*{uan} + ({delivery_china}+{delivery_moscow}+{commission}) = {x[message.from_user.id]}""".format(message.from_user), reply_markup = markup_cost)
    
    except:  
        markup_cost = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back1 = types.KeyboardButton('🔴 Начать заново')
        markup_cost.add(back1)
        bot.send_message(message.chat.id, 'Некорректная сумма'.format(message.from_user), reply_markup = markup_cost)
        

def bot_message_name(message):
    
    if message.text == '🔴 Начать заново':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
    else:
        global username
        username[message.from_user.id] = '@' + message.from_user.username
        global name
        name[message.from_user.id] = message.text
        cancel = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back1 = types.KeyboardButton('🔴 Начать заново')
        cancel.add(back1)
        message_phone = bot.send_message(message.chat.id, 'Продолжим. Теперь нам нужно уточнить номер телефона по которому мы сможем с вами связаться. Введите номер:'.format(message.from_user), reply_markup = cancel)
        bot.register_next_step_handler(message_phone,bot_message_phone)
    
def bot_message_phone(message):
    
    if message.text == '🔴 Начать заново':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
    else:
        global phone
        phone[message.from_user.id] = message.text
        cancel = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back1 = types.KeyboardButton('🔴 Начать заново')
        cancel.add(back1)
        message_link = bot.send_message(message.chat.id, 'Пришлите ссылку на товар, который хотите заказать:'.format(message.from_user), reply_markup = cancel)
        bot.register_next_step_handler(message_link,bot_message_link)

def bot_message_link(message):
    
    if message.text == '🔴 Начать заново':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
    else:
        global link
        link[message.from_user.id] = message.text
        cancel = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back1 = types.KeyboardButton('🔴 Начать заново')
        cancel.add(back1)
        message_size = bot.send_message(message.chat.id, 'Укажите размер для данного товара:'.format(message.from_user), reply_markup = cancel)
        bot.register_next_step_handler(message_size,bot_message_size)
    
def bot_message_size(message):
    
    if message.text == '🔴 Начать заново':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
    else:
        global size
        size[message.from_user.id] = message.text
        markup_delivery = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1_delivery = types.KeyboardButton('Самовывоз: г.Москва, Хорошевское шоссе 72к4')
        item2_delivery = types.KeyboardButton('Доставка по РФ')
        item3_delivery = types.KeyboardButton('🔴 Начать заново')
        markup_delivery.add(item1_delivery, item2_delivery, item3_delivery)
        message_delivery = bot.send_message(message.chat.id, 'Выберите способ доставки:'.format(message.from_user), reply_markup = markup_delivery)
        bot.register_next_step_handler(message_delivery,bot_message_delivery)
           
def bot_message_delivery(message):
    
    if message.text == '🔴 Начать заново':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
    elif message.text == 'Самовывоз: г.Москва, Хорошевское шоссе 72к4':
        global delivery
        delivery[message.from_user.id] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        
        bot.send_message(message.chat.id, f"""Ваш заказ:
Фамилия Имя: {name[message.from_user.id]}
Номер телефона: {phone[message.from_user.id]}
Ссылка на товар: {link[message.from_user.id]}
Размер: {size[message.from_user.id]}
Способ доставки: {delivery[message.from_user.id]}

Ждем вас снова!""".format(message.from_user), reply_markup = markup)

        bot.send_message(id_admin, f"""Новый заказ:
Телеграм: {username[message.from_user.id]}
Фамилия Имя: {name[message.from_user.id]}
Номер телефона: {phone[message.from_user.id]}
Ссылка на товар: {link[message.from_user.id]}
Размер: {size[message.from_user.id]}
Способ доставки: {delivery[message.from_user.id]}""")
    else:
        cancel = types.ReplyKeyboardMarkup(resize_keyboard = True)
        back1 = types.KeyboardButton('🔴 Начать заново')
        cancel.add(back1)
        message_address = bot.send_message(message.chat.id, 'Введите адрес доставки:'.format(message.from_user), reply_markup = cancel)
        bot.register_next_step_handler(message_address,bot_message_address)
        
def bot_message_address(message):
    
    if message.text == '🔴 Начать заново':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Чем могу помочь?'.format(message.from_user), reply_markup = markup)
    else:
        global delivery
        delivery[message.from_user.id] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('🔐 Получить инструкцию')
        item2 = types.KeyboardButton('💵 Рассчитать стоимость')
        item3 = types.KeyboardButton('🔥 Оформить заказ')
        markup.add(item1, item2, item3)
        
        bot.send_message(message.chat.id, f"""Ваш заказ:
Фамилия Имя: {name[message.from_user.id]}
Номер телефона: {phone[message.from_user.id]}
Ссылка на товар: {link[message.from_user.id]}
Размер: {size[message.from_user.id]}
Способ доставки: {delivery[message.from_user.id]}

Ждем вас снова!""".format(message.from_user), reply_markup = markup)

        bot.send_message(id_admin, f"""Новый заказ:
Телеграм: {username[message.from_user.id]}
Фамилия Имя: {name[message.from_user.id]}
Номер телефона: {phone[message.from_user.id]}
Ссылка на товар: {link[message.from_user.id]}
Размер: {size[message.from_user.id]}
Способ доставки: {delivery[message.from_user.id]}""")

bot.polling(none_stop = True)
