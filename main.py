import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handler, other_handler


async def main() -> None:
    dp = Dispatcher()
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handler.router)
    dp.include_router(other_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

