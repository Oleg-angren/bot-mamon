import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Не установлен BOT_TOKEN в .env файле")

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Привет! Я бот, который работает 24/7 на Render.com!")

# Обработчик /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Пока что я только отвечаю на /start и повторяю твои сообщения.")

# Эхо-обработчик
@dp.message()
async def echo(message: types.Message):
    try:
        await message.answer(f"«{message.text}» — ты сказал? Запомню! 😄")
    except Exception as e:
        logger.error(f"Ошибка при ответе: {e}")

# Основная функция
async def main():
    logger.info("Бот запускается...")
    try:
        # Удаляем вебхук, если был
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен в режиме polling. Ожидание сообщений...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            close_bot_after=True
        )
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
