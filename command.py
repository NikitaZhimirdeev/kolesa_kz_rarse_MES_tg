from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import requests
from bs4 import BeautifulSoup as BS4
from create_bot import dp, bot, dir_path
import config
import os
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class UPDATE(StatesGroup):
    typeofsearch = State()
    REG = State()
    follow = State()


class READ(StatesGroup):
    start_com = State()


@dp.message_handler(commands='look', state=None)
async def main(message: types.Message, state: FSMContext):
    await READ.start_com.set()

    with open(os.path.join(dir_path, 'regions.txt'), 'r') as file:
        regions = ''.join(file.readlines()).strip().split('\n')

    mes = 'Регионы за которыми происходит мониторинг\n\n'
    for reg in regions:
        mes += f'{reg} - {config.URLS_reg[reg]["name"]} - {config.URLS_reg[reg]["href"]}\n'

    mes = mes.strip('\n')

    await bot.send_message(chat_id=message.from_user.id, text=mes)
    await state.finish()


# @dp.message_handler(commands='update', state=None)
async def cm_update(message: types.Message):
    await UPDATE.typeofsearch.set()

    with open(os.path.join(dir_path, 'regions.txt'), 'r') as file:
        regions = ''.join(file.readlines()).strip().split('\n')

    mes = 'Регионы за которыми происходит мониторинг\n\n'
    for reg in regions:
        mes += f'{reg} - {config.URLS_reg[reg]["name"]} - {config.URLS_reg[reg]["href"]}\n'

    mes = mes.strip('\n')

    await bot.send_message(chat_id=message.from_user.id, text=mes)

    mes = 'Введите номера регионов, за которыми необходимо следить\n' \
          'Вводить необходимо через запятую\n' \
          'Пример: 1, 2,3\n\n'
    for r in config.URLS_reg:
        mes += f"{r} - {config.URLS_reg[r]['name']}\n"

    mes += f'\nДля отмены данного дествия просто ввелите "отмена"'

    await bot.send_message(chat_id=message.from_user.id, text=mes)


@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    # if message.from_user.id == ID:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


@dp.message_handler(state=UPDATE.typeofsearch)
async def find_name(message: types.Message, state: FSMContext):
    regs = message.text.split(',')

    with open(os.path.join(dir_path, 'regions.txt'), 'w') as file:
        for reg in regs:
            file.write(f'{reg.strip()}\n')

    await state.finish()



def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_update, commands='update', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(main, commands='look', state=None)
