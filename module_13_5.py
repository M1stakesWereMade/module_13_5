from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button2 = KeyboardButton(text = 'Расчитать')
button = KeyboardButton(text = 'Информация')
kb.add(button2)
kb.add(button)

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Информация')
async def inform(message: types.Message):
    await message.answer('Информация о боте!')

@dp.message_handler(text = 'Расчитать')
async def set_age(message: types.Message):
    await message.answer('Напишите свой возраст:')
    await UserState.age.set()
        
@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')

@dp.message_handler(state = UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = float(data.get('age'))
    growth = float(data.get('growth'))
    weight = float(data.get('weight'))
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал")
    await state.finish()
    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)