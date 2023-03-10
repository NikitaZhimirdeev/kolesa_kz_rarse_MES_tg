from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

# Получаем полный путь к дирректории
dir_path = os.path.dirname(os.path.abspath(__file__))