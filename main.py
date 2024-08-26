import logging
import ssl
import sys
import os
from dotenv import load_dotenv

from aiohttp import web
from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_PATH = '/websocket'
DOMAIN = os.getenv('DOMAIN')
EXTERNAL_PORT = 80
BASE_WEBHOOK_URL = "https://" + DOMAIN + ":" + str(EXTERNAL_PORT)
WEB_SERVER_HOST = DOMAIN
WEB_SERVER_PORT = EXTERNAL_PORT
WEBHOOK_SECRET = "my-secret"
WEBHOOK_SSL_CERT = "cert.pem"
WEBHOOK_SSL_PRIV = "key.key"


router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        certificate=FSInputFile(WEBHOOK_SSL_CERT),
        secret_token=WEBHOOK_SECRET)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

     # ==== For self-signed certificate ====
        # Generate SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

        # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, ssl_context=context)
    # else:
        # And finally start webserver
        # web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()

# ================ Creating a self-signed certificate =============================
# openssl req -newkey rsa:2048 -sha256 -nodes -keyout SSL/PRIVATE_self.key -x509 -days 365
# -out SSL/PUBLIC_self.pem -subj "/C=RU/ST=RT/L=KAZAN/O=Home/CN=217.18.63.197"
# =============== For values from .env file ============================================
# from dotenv import load_dotenv, dotenv_values
# config = dotenv_values(".env_dev")
# DOMAIN = config['DOMAIN_NAME']
# FROM_ENV_FILE = True
# =================================================================================
# from decouple import AutoConfig
# config = AutoConfig()
