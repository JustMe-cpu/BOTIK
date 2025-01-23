import asyncio
import os
from multiprocessing.connection import answer_challenge
from pkgutil import get_data
from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv
from pydantic.v1 import root_validator
from States import Survey
from keybord import reply_kb
from keybord import inline_kbgit

load_dotenv()
bot_token=os.getenv("TOKEN")


bot = Bot(token=bot_token)
dp = Dispatcher()
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Выберите опцию:", reply_markup=reply_kb)

@router.message(Command(commands='help'))
async def cmd_help(message: Message):
    await message.answer(f"ПРИВЕТ! {message.from_user.first_name} Сам не справишься?")

@router.message(Command(commands='info'))
async def cmd_info(message: Message):
    txt = ("Приветствую! Я-БотяраV1.\n"
           "Пока что я умею кидать ссылки, принимать фотографии,но в следующих вресиях... \n"
           "будет намного больше!\n"
           "<b>Мои команды:</b>\n"
           "/help = помощь\n"
           "/google = Ссылка на гугл \n"
           "<i>Удачи!</i>")
    await message.reply(f"{txt}", parse_mode="HTML")

@router.message(Command(commands='inet'))
async def cmd_inet(message: Message):
    await message.answer(f"Вот ссылки", reply_markup=inline_kb)

@router.message(Command('google'))
async def cmd_gogogole(message: Message):
    await message.answer(f"[here](https://google.com)", parse_mode="MarkdownV2")

@router.message(Command(commands="survey"))
async def cmd_survey(message: Message, state: FSMContext):
    await message.answer(f"Как вас зовут?")
    await state.set_state(Survey.name)

@router.message(Survey.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Сколько вам лет?")
    await state.set_state(Survey.age)

@router.message(Survey.age, F.text)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Какой ваш любимый цвет?")
    await state.set_state(Survey.color)

@router.message(Survey.color, F.text)
async def process_color(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    color = message.text
    answer_text = f"""
Отлично!!!\n
Спасибо за пройденный опрос!!!\n
Ваш любимый возраст: {age}\n
Вас зовут: {color}\n
Ваш любимый цвет: {name}\n"""
    await message.answer(answer_text)
    await state.clear()



@router.message(F.text == "Жив?")
async def reply_text(message: Message):
    await message.reply(f"Да, а ты?")

@router.message(F.text)
async def reply_text(message: Message):
    if len(message.text) > 20:
        await message.reply("Чё так много? Мне лень это обрабатывать.")
    else:
        await message.reply(f"Ты написал {message.text}")

@router.message(F.photo)
async def reply_image(message: Message):
    await message.answer(f"Красиво.")

async def main():
    print("starting bot...")
    dp=Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())