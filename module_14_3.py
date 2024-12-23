from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import asyncio


api = "7169846208:AAHUXg22pIVPN873wMhCF90Cgm6EGUQgOYI"
bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())


kb = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.add(button1)
kb.add(button2)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Рассчитать')
button4 = KeyboardButton(text='Информация')
button5 = KeyboardButton(text='Купить')
kb1.row(button3,button4)
kb1.add(button5)

pr_kb = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text='Product1',
                             callback_data='product_buying'),
        InlineKeyboardButton(text='Product2',
                             callback_data='product_buying'),
        InlineKeyboardButton(text='Product3',
                             callback_data='product_buying'),
        InlineKeyboardButton(text='Product4',
                             callback_data='product_buying')
    ]]
)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb1)

@dp.message_handler(text='Рассчитать')
async def start_message(message):
    await message.answer('выберите опцию:', reply_markup=kb)

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Название: Product{i} | '
                             f'Описание: описание {i} | '
                             f'Цена: {i * 100}')
        with open(f'product_photo{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:',
                         reply_markup=pr_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
   # data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
   # data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    result = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий {result}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)