from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())
rep_kb = ReplyKeyboardMarkup(resize_keyboard = True)
rep_bt1 = KeyboardButton(text = 'Рассчитать')
rep_bt2 = KeyboardButton(text = 'Информация')
rep_kb.add(rep_bt1)
rep_kb.add(rep_bt2)
inline_kb = InlineKeyboardMarkup()
inline_bt1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
inline_bt2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
inline_kb.add(inline_bt1)
inline_kb.add(inline_bt2)

@dp.message_handler(commands = ['start'])
async def all_messages(message):
    await message.answer('Привет! я бот, помогающий твоему здоровью.', reply_markup = rep_kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup= inline_kb )

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 \n '
                      'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_age(message, state):
    await state.update_data(weight = message.text)
    await message.answer('Введите свой пол (М/Ж):')
    await UserState.sex.set()

@dp.message_handler(state = UserState.sex)
async def send_calories_male(message, state):
    await state.update_data(sex=message.text)
    data = await state.get_data()
    if data['sex'] == 'М':
        calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    if data['sex'] == 'Ж':
        calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    await message.answer(f'Вам требуется {calories} калорий в день')


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)