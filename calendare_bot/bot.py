import asyncio
import re
import locale

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram_calendar import SimpleCalendar, DialogCalendar, SimpleCalendarCallback, get_user_locale
from config import Config
import db

conf = Config()

bot = Bot(token=conf.token)
dp = Dispatcher()

main_menu = InlineKeyboardMarkup(inline_keyboard=conf.menu)

# Проверка на администратора
def check_admin(chat_id) -> bool:
    if chat_id in conf.admins:
        return True
    return False


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if check_admin(message.chat.id) == False:
        await message.answer("Извините бота пока находится в альфа тесте\nДоступ только у некоторых пользователей")
        return
    await message.answer(text=f"Привет {message.from_user.first_name} \nВыберите что необходимо", reply_markup=main_menu)


@dp.message()
async def test(msg: types.Message):
    await msg.answer(
        text=f"Я не знаю комманду {msg.text} \nВыберите что необходимо", 
        reply_markup=main_menu
        )


@dp.callback_query(F.data == "get_calendar")
async def get_calendar(callback: types.CallbackQuery):
    await callback.message.answer(
            "Вот ваш календарь, выберите дату: \n",
            reply_markup=await SimpleCalendar().start_calendar()
        )


@dp.callback_query(F.data == "check_date")
async def get_now_date(callback: types.CallbackQuery):
    await callback.message.answer("Вот что у тебя сегодня: ")
    res = db.get_events()
    if len(res) == 0:
        await callback.message.answer("На эту дату нету событий")
        return
    for i in res:
        await callback.message.answer(str(i))
    return


@dp.callback_query(SimpleCalendarCallback.filter())
async def select_date(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Ваша выбранная дата: {date.strftime("%d/%m/%Y")} \n'
        )
    events = db.get_by_day(date)
    if len(events) == 0:
        await callback_query.message.answer("На эту дату нету событий")
        return
    for i in events:
        await callback_query.message.answer(str(i))
    return

# @dp.callback_query(F.data=="add_event")
# async def add_event(callback: types.CallbackQuery):
#     await callback.message.answer(
#         "Выберите дату \n",
#         reply_markup=await SimpleCalendar().start_calendar()
#         )

# Начинаем запрашивать обновления у бота
async def main():
    await dp.start_polling(bot)

# При запуске программы, запускаем процедуру main
if __name__ == "__main__":
    asyncio.run(main())
