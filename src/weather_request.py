import requests


from datetime import datetime


from utils.url_data import URL_WEATHER_REQUEST


def weather_client() -> dict | None:
    url = URL_WEATHER_REQUEST
    params = {
        "latitude": 58.5966,
        "longitude": 49.6601,
        "hourly": "temperature_2m,precipitation_probability,relative_humidity_2m,precipitation,rain",
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            print("Ошибка: пустой ответ")
            return None

        return data
    
    except requests.RequestException as e:
        print(f"Ошибка запроса (интернет/DNS/таймаут/HTTP): {e}")
        return None
    except ValueError:
        print("Ошибка: сервер вернул не JSON")
        return None
    

def print_weather_at_9(data: dict) -> str | None:
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    pops = hourly.get("precipitation_probability", [])
    prcps = hourly.get("precipitation", [])
    rains = hourly.get("rain", [])

    if not times:
        print("Не нашел данных по часам")
        return None
    
    idx = next((i for i, t in enumerate(times) if t.endswith("T09:00")), None)
    if not idx:
        print("На 09:00 данных нет")
        return None
    
    dt = datetime.fromisoformat(times[idx])
    date_str = dt.strftime("%d.%m.%Y")

    text_weather_at_9 = (
        "☀️Прогноз погоды на сегодня:\n"
        f"🌡️На 09:00 ({date_str}): {temps[idx]:.1f}°C.\n"
        f"🌧️Шанс осадков — {pops[idx]}%.\n"
        f"💧Ожидается осадков: {prcps[idx]:.1f} мм (дождь: {rains[idx]:.1f} мм)."
    )
    
    return text_weather_at_9


async def weather_output() -> str:
    data = weather_client()
    text = print_weather_at_9(data)
    return text