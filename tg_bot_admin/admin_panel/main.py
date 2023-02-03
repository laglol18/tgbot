from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from . import models
from . import buttons

#Для работы с ботом
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"



class Registration(StatesGroup):
    getting_name = State()
    getting_number = State()
    getting_service = State()
    getting_meet_format = State()

bot = Bot(token='6011056539:AAFIH7wQOM-jsc4CXZdiU9POiEBl93gpWfc')
dp = Dispatcher(bot=bot, storage=MemoryStorage())

#/start
@dp.message_handler(commands=['start'], state='*')
async def start_message(message):

    checker = models.TgUser.objects.filter(telegram_id=message.from_user.id).exists()

    if not checker: #Если нет пользователя
        await message.answer('Привет')

        await Registration.getting_name.set()
    else:  #Если есть
        await message.answer('Какую услугу хотите заказать?', reply_markup=buttons.send_service_button())
        await Registration.getting_service.set()
#Этап получения имени
@dp.message_handler(content_types=['text'], state=Registration.getting_name)
async def text_messages(message, state: Registration.getting_name):
    name = message.text

    await state.update_data(username=name)

    await message.answer('Теперь номер', reply_markup=buttons.number_button())
    await Registration.getting_number.set() #Этап получения услуги

@dp.message_handler(content_types=['text', 'contact'], state=Registration.getting_number)
async def get_number(message, state: Registration.getting_number):
    number = message.text or message.contact.phone_number

    await state.update_data(phone_number=number)

    await message.answer('Теперь услуга', reply_markup=buttons.send_service_button())
    await Registration.getting_service.set()
@dp.message_handler(content_types=['text', 'contact'], state=Registration.getting_service)
async def get_user_service(message, state: Registration.getting_service):

    service = message.text

    all_services = [i.service_name for i in models.Services.objects.all()]


    if service in all_services:

        checker = models.TgUser.objects.filter(telegram_id=message.from_user.id).exists()

        service_from_db = models.Services.objects.get(service_name=service)

        await message.answer('Заявка успешно создана, ожидайте ответа')

        get_all_data = await  state.get_data()
        if not checker:
            user_name = get_all_data['username']
            user_number = get_all_data['phone_number']

            user = models.TgUser(telegram_id=message.from_user.id,
                          user_name=user_name,
                          user_phone_number=user_number).save()

            models.TgOrders(telegram_id=user, user_service=service_from_db) .save()

        else:
            user = models.TgUser.objects.get(telegram_id=message.from_user.id)
            models.TgOrders(telegram_id=user, user_service=service_from_db).save()
        await  bot.send_message(5495523009, 'Новый заказ')

        await state.finish()

    else:
        await  message.answer('Ошибка в данных\nОтправьте команду /start')

        await state.finish

