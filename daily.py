# keyboard = types.ReplyKeyboardRemove() # удалить клавиатуру
import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
# from aiogram.enums import ParseMode
# from daily_db import answers save_info

TOKEN = "7644799185:AAHEFF2mvXWl5plIzPtb9m04SgPzJgCudTA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
tasks = [
    "X Отжимание: 100 раз",
    "X Приседание: 100 раз",
    "X Пресс качание: 100 раз",
    "X Бег: 10 км",
]

@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or message.text == "/start" or message.text == "Start again":
        await start(message)
    elif "" not in user_data[user_id]:
        pass


@dp.message(Command("start"))               # вызвать функцию на следующей строке
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    buttons = []
    for i in range(len(tasks)):
        buttons.append([types.InlineKeyboardButton(text=f"{tasks[i]}", callback_data=f"task_{i}")])
    buttons.append([types.InlineKeyboardButton(text=f"Сохранить", callback_data=f"save_-1")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
    await message.answer("Список задач на сегодня", reply_markup=keyboard)
    print(user_data)


@dp.callback_query(lambda c: c.data.startswith(('task', 'save', 'change')))
async def check_callback_data(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    command, detail = callback.data.split("_")
    text = "Список задач на сегодня:"
    buttons = []

    if command == "task":
        i = int(detail)
        n = len(tasks[i])
        # if tasks[i][0:2] == "~~":
        #     tasks[i] = tasks[i][2:n-2]
        # else:
        #     tasks[i] = "~~" + tasks[i] + "~~"
        if tasks[i][0] == "X":
            tasks[i] = "V" + tasks[i][1:n]
        elif tasks[i][0] == "V":
            tasks[i] = "X" + tasks[i][1:n]
        for i in range(len(tasks)):
            buttons.append([types.InlineKeyboardButton(text=f"{tasks[i]}", callback_data=f"task_{i}")])
        buttons.append([types.InlineKeyboardButton(text=f"Сохранить", callback_data=f"save_-1")])

    elif command == "save":
        for task in tasks:
            text += "\n\n" + task
        buttons.append([types.InlineKeyboardButton(text=f"Изменить", callback_data=f"change_-1")])

    elif command == "change":
        for i in range(len(tasks)):
            buttons.append([types.InlineKeyboardButton(text=f"{tasks[i]}", callback_data=f"task_{i}")])
        buttons.append([types.InlineKeyboardButton(text=f"Сохранить", callback_data=f"save_-1")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except:
        pass



# @dp.message(Command("menu"))
# async def menu(message: types.Message):
#     user_id = message.from_user.id
#     language = user_data[user_id]["language"]
#     buttons = [
#         [types.InlineKeyboardButton(text=f"Русский", callback_data=f"lang_Русский"),
#          types.InlineKeyboardButton(text=f"English", callback_data=f"lang_English")],
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
#     answer = answers["menu"][language]
#     await message.answer(answer, reply_markup=keyboard)
#     print(user_data)
#
#
# async def change_lang(message: types.Message):
#     user_id = message.from_user.id
#     language = user_data[user_id]["language"]
#     buttons = [
#         [types.InlineKeyboardButton(text=f"Русский", callback_data=f"lang_Русский"),
#          types.InlineKeyboardButton(text=f"English", callback_data=f"lang_English")],
#         [types.InlineKeyboardButton(text=f"{answers["back"][language]}", callback_data=f"back_none")]
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True)
#     answer = answers["language"][language]
#     await message.answer(answer, reply_markup=keyboard)
#     print(user_data)


async def main():
    await dp.start_polling(bot)


print("Bot is running...")
asyncio.run(main())
