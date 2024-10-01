import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.handlers import router
from app.middleware.rate_limit import RateLimitMiddleware


async def main():
    logging.info("Starting async_main to create tables")
    load_dotenv()
    bot = Bot(token='7328368140:AAFtbtyF3gTGVG_l2NjIl2t4cUX3LxKmIVw')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.update.middleware(RateLimitMiddleware(limit=2))
    logging.info("Starting bot polling")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())