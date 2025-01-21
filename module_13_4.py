from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()
api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

@dp.message_handler(commands=['start'])
async def all_messages(message):
    await message.answer('Привет! я бот, помогающий твоему здоровью.')

@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
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
    await state.update_data(weight=message.text)
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