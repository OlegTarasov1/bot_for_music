from settings.logg_settings import logger
import asyncio
import os
from views import master_router
from aiogram import (
    Bot,
    Dispatcher
)


async def main():
    bot = Bot(token = os.getenv("BOT_TOKEN"))

    dp = Dispatcher()
    logger.info("PROJECT START...\n\n\n")
    dp.include_router(master_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())