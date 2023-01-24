import asyncio
import time
from create_bot import dp, bot, dir_path
from aiogram import executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from multiprocessing import Process
import os
import config
import modules

if 'users.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'users.txt'), 'a') as f:
            pass

if 'All.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'All.txt'), 'a') as f:
            pass

# Идексация того, что бот начал работу
async def on_startup(_):
    print('Бот вышел в сеть')

# Команда запуска бота
@dp.message_handler(commands=['start'])
async def START(message: types.Message):
    # Сбор всех id пользователей, которые активировали бота
    with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
        users = ''.join(f.readlines()).strip().split('\n')

    # Проверка, если пользователя нет в списке активировавших, то записываем его туда
    if not (str(message.from_user.id) in users):
        with open(os.path.join(dir_path, 'users.txt'), 'a') as f:
            f.write(f'{message.from_user.id}\n')

    await message.answer('Здравствуйте! Данный ботследитза ценами на сайте kolesa.kz.\n'
                         'Чтобы посмотретьвозможности бота введите команду /help')

# Команда запуска бота
@dp.message_handler(commands=['help'])
async def HELP_fol(message: types.Message):
    await message.answer("/update - удалить регион из мониторинга\n"
                         "/look - Команда для просмотра регионов мониторинга")


import command
command.register_handlers_admin(dp)

async def PARSER_WHILE():
    while True:
        with open(os.path.join(dir_path, 'regions.txt'), 'r') as file:
            regions = ''.join(file.readlines()).strip().split('\n')

        for url_reg in regions:
            with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
                users = ''.join(f.readlines()).strip().split('\n')

            with open(os.path.join(dir_path, 'All.txt'), 'r') as f:
                All = ''.join(f.readlines()).strip().split('\n')

            print(config.URLS_reg[url_reg]["href"])
            print(config.URLS_reg[url_reg]["name"])
            print()

            # last_page = modules.find_last_page(url_reg)

            INFO_in_one_page = []

            # for page in range(1, last_page + 1):  # last_page + 1
            url_page = f'{config.URLS_reg[url_reg]["href"]}&page=1'
            print(url_page)

            INFO_in_one_page = modules.find_info_in_page(url_page)

            for INFO in INFO_in_one_page:
                if INFO["href"] not in All:
                    MES = modules.create_mes(INFO)
                    for user in users:
                        try:
                            await bot.send_message(chat_id=user, text=MES)
                            await asyncio.sleep(1)
                        except:
                            pass

                    All.append(INFO["href"])
                    with open(os.path.join(dir_path, 'All.txt'), 'a') as f:
                        f.write(f'{INFO["href"]}\n')
            await asyncio.sleep(10)

        await asyncio.sleep(300)


def Bot1():
    loop = asyncio.get_event_loop()
    loop.create_task(PARSER_WHILE())
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    p1 = Process(target=Bot1)
    p1.start()
    time.sleep(85800)
    p1.kill()
