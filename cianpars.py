import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from bot import *


load_dotenv()


async def start():

    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())