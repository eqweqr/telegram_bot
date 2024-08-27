from aiogram import Dispatcher, Bot, Router
import fastapi
from aiogram.filters import Command
from aiogram.types import BotCommand, FSInputFile, Message
from aiogram.enums import ParseMode
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
DOMAIN = os.getenv('DOMAIN')
WEBHOOK_PATH = '/webhook'
EXTERNAL_PORT = 80
BASE_WEBHOOK_URL = "https://" + DOMAIN + ":" + str(EXTERNAL_PORT)
WEB_SERVER_HOST = DOMAIN
WEB_SERVER_PORT = EXTERNAL_PORT
WEBHOOK_SECRET = "my-secret"
WEBHOOK_SSL_CERT = "cert.pem"
WEBHOOK_SSL_PRIV = "key.key"

bot = Bot(token=TOKEN)
router = Router(name='telegram')


dp = Dispatcher()

@router.message(Command('/id'))
async def id_command(message: Message):
    await message.answer(f'{message.from_user.id}')
    
@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

dp.include_router(router)

async def set_bot_commands_menu(my_bot: Bot) -> None:
    # Register commands for Telegram bot (menu)
    commands = [
        BotCommand(command="/id", description="👋 Get my ID"),
    ]
    try:
        await my_bot.set_my_commands(commands)
    except Exception as e:
        print(f"Can't set commands - {e}")

@asynccontextmanager
async def startup_down(app: fastapi.FastAPI):
    await bot.set_webhook(
        f'{BASE_WEBHOOK_URL}{WEBHOOK_PATH}',
        certificate=FSInputFile(WEBHOOK_SSL_CERT),
    )
    set_bot_commands_menu(bot)
    yield
    await bot.delete_webhook()