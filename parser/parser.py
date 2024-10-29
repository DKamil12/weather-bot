import requests
import logging


def get_json(city: str, interval: str, days: str = 0) -> dict | None:
    API_KEY = '37344f15a545419a9d8154159242204'
    url = f'http://api.weatherapi.com/v1/{interval}.json?key={API_KEY}&q={city}&days={days}&aqi=no&alerts=no'

    try:
        # Make API request and parse JSON 
        request = requests.get(url)
        json_data = request.json()
        return json_data
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Something went wrong when trying to connect {url}: {e}')
        return None
    except Exception as e:
        logging.error(f'Something went wrong, error: {e}')
        return None


def parse_current_weather(json_data: dict) -> dict:
    current_weather = {
        'icon': f"https:{json_data['current']['condition']['icon']}",
        'temp': f"{json_data['current']['temp_c']}°C, {json_data['current']['condition']['text']}",
        'wind': f"{json_data['current']['wind_mph']} m/h",
        'humidity': f"{json_data['current']['humidity']}%"
    }
    return current_weather


def parse_forecast(json_data: dict) -> list:
    # list to store every forecast separately
    forecast = []

    for day in json_data['forecast']['forecastday']:
        # every day is stored in single dict
        forecast_day = {
            'date': day['date'],
            'day_temp': f"{day['day']['maxtemp_c']}°C, {day['day']['condition']['text']}",
            'night_temp': f"{day['day']['mintemp_c']}°C",
            'wind': f"{day['day']['maxwind_mph']} m/h",
            'humidity': f"{day['day']['avghumidity']}%"
        }
        forecast.append(forecast_day)

    return forecast


def get_current_weather(city: str, interval: str) -> dict | None:
    json = get_json(city, interval)
    
    if json:
        # parse current weather details and convert them to convenient form
        curr_weather = parse_current_weather(json)
        icon = curr_weather['icon']
        text = (
            f"Temperature: {curr_weather['temp']}\n"
            f"Wind: {curr_weather['wind']}\n"
            f"Humidity: {curr_weather['humidity']}"
        )

        return {'icon': icon, 'text': text}
    else:
        return None


def get_forecast(city: str, interval: str, days: str) -> str | None:
    json = get_json(city, interval, days)

    if json:
        # parse forecast details and convert them to convenient form
        forecast = parse_forecast(json)

        forecast_items = []
        for day in forecast:
            forecast_item = (
                f"Date: {day['date']}\n"
                f"Day Temperature: {day['day_temp']}\n"
                f"Night Temperature: {day['night_temp']}\n"
                f"Wind: {day['wind']}\n"
                f"Humidity: {day['humidity']}\n"
            )
            forecast_items.append(forecast_item)
        
        # convert a list with forecast items to string
        text = '\n'.join(forecast_items)

        return text
    else:
        return None