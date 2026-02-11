import requests


from utils.url_data import URL_RANDOM_QUOTE_REQUESTS
from utils.url_data import URL_MYMEMORY_GET


def fetch_quote() -> tuple[str, str] | None:
    url = URL_RANDOM_QUOTE_REQUESTS

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            print("JSON пуст")
            return None

        q = data[0]["q"]
        a = data[0]["a"]

        if not q or not a:
            print("Ошибка: нет ключей 'q'/'a' в ответе ZenQuotes")
            return None

        return q, a

    except requests.RequestException as e:
        print(f"Ошибка запроса (интернет/DNS/таймаут/HTTP): {e}")
        return None
    except ValueError:
        print("Ошибка: сервер вернул не JSON")
        return None
    

def translate_mymemory(text: str, source: str = "en", target: str = "ru") -> str | None:
    url = URL_MYMEMORY_GET
    params = {
        "q": text,
        "langpair": f"{source}|{target}",
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        payload = resp.json()

    except requests.RequestException as e:
        print(f"Ошибка запроса (интернет/DNS/таймаут/HTTP): {e}")
        return None
    except ValueError:
        print("Ошибка: сервер вернул не JSON")
        return None
    
    translated = (payload.get("responseData") or {}).get("translatedText")

    if not translated:
        print("Ошибка: MyMemory вернул пустой перевод")
        return None
    
    return translated


async def quote_client_ru() -> str | None:
    quote = fetch_quote()
    if not quote:
        return None
    
    q_en, author = quote
    q_ru = translate_mymemory(q_en, source="en", target="ru")

    if q_ru:
        text_ru = (
            "💡Цитата дня на сегодня:\n"
            f"{q_ru} — {author}")
        return text_ru