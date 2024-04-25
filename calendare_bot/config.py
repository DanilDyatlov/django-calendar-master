from aiogram.types import InlineKeyboardButton

class Config:
    def __init__(self):
        self.admins = [571299800, 778665071]
        self.token = '6856600764:AAGSNHZpW3tgSnpqJoz_62eFJfokn2Pt9SQ'
        self.menu = [
            [InlineKeyboardButton(text="Что на сегодня", callback_data="check_date")],
             [InlineKeyboardButton(text="Кадендарь", callback_data="get_calendar")],
        ]