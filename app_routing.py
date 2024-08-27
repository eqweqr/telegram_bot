import fastapi
from tg_bot import dp, bot
from aiogram import types
from tg_bot import WEBHOOK_PATH

route = fastapi.APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)

@route.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)
    