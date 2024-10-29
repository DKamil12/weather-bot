from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from kb import generator
from parser.parser import get_current_weather, get_forecast

router = Router()

class WeatherStates(StatesGroup):
    city = State()
    interval = State()
    forecast_days = State()

@router.message(Command('get_weather'))
async def search_start(msg: Message, state: FSMContext):
    await state.set_state(WeatherStates.city)
    await msg.answer(
        'Please select your city below:', reply_markup=generator.generate_kb(['Almaty', 'Astana', 'Pavlodar', 'Semey']))
    

@router.message(WeatherStates.city)
async def set_city(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await state.set_state(WeatherStates.interval)

    await msg.answer('Do you want to get the current weather or forecast?', reply_markup=generator.generate_kb(['Current', 'Forecast']))


@router.message(F.text.lower() == 'current')
async def show_current_weather(msg: Message, state: FSMContext):
    await state.update_data(interval=msg.text.lower())
    data = await state.get_data()
    weather = get_current_weather(city=data['city'], interval=data['interval'])

    # if weather is not None, send it to user, else send error message
    if weather:
        await msg.answer_photo(photo=weather['icon'], 
                            caption=f'The weather in {data["city"]} right now: \n{weather['text']}', 
                            reply_markup=generator.generate_kb(['/get_weather']))
    else:
        await msg.answer('Something went wrong, please try later!')

    await state.clear()
    

@router.message(F.text.lower() == 'forecast')
async def select_forecast_days(msg: Message, state: FSMContext):
    await state.update_data(interval=msg.text.lower())
    await state.set_state(WeatherStates.forecast_days)

    await msg.answer('Choose forecast days:', reply_markup=generator.generate_kb(['1', '2', '3']))


@router.message(WeatherStates.forecast_days)
async def show_forecast(msg: Message, state: FSMContext):
    await state.update_data(days=msg.text)
    data = await state.get_data()
    forecast = get_forecast(city=data['city'], interval=data['interval'], days=data["days"])

    # if weather is not None, send it to user, else send error message
    if forecast:
        await msg.answer(f'Weather forecast in {data["city"]} for {data['days']} day(s): \n\n{forecast}', reply_markup=generator.generate_kb(['/get_weather']))
    else:
        await msg.answer('Something went wrong, please try later!')

    await state.clear()
