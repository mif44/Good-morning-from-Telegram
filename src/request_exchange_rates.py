import requests


from utils.url_data import URL_REQUESTS_EXCHANGE_RATES


async def fx_client() -> dict | None:
    url = URL_REQUESTS_EXCHANGE_RATES
    params = {
        "symbols": "USD,EUR,CNY",
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            print("JSON пуст")
            return None

        rates = data.get("rates", {})
        rub_usd = rates.get("USD")
        rub_eur = rates.get("EUR")
        rub_cny = rates.get("CNY")

        if rub_usd and rub_eur and rub_cny:
            rates_text = (
            "🪙Курс валют на сегодня:\n"
            f"💵Доллар:{1/rub_usd:.2f} RUB\n"
            f"💶Евро:{1/rub_eur:.2f} RUB\n"
            f"💴Юань:{1/rub_cny:.2f} RUB"
            )
            return rates_text
        else:
            print(f"Нет валют.")
            return None

    
    except requests.RequestException as e:
        print(f"Ошибка запроса (интернет/DNS/таймаут/HTTP): {e}")
        return None
    except ValueError:
        print("Ошибка: сервер вернул не JSON")
        return None
    
