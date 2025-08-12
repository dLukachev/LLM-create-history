import os
import aiohttp
from dotenv import load_dotenv
import json
import logging

load_dotenv()

MODEL = os.getenv('MODEL')
KEY = os.getenv('OPENROUTER_KEY')
URL = os.getenv('URL_ROUTER')

class OpenRouterService:

    def __init__(self, api_key=KEY, model=MODEL, url=URL) -> None:
        self.api_key = api_key
        self.model = model
        self.url = url
        self.messages = []

    async def call(self, prompt, role="user"):
        # Добавляем новое сообщение пользователя
        self.messages.append({"role": role, "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": self.messages
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=headers, data=json.dumps(payload)) as response: # type: ignore
                    # Проверка статуса
                    if response.status != 200:
                        text = await response.text()
                        logging.error(f"HTTP error {response.status}: {text}")
                        return f"Ошибка HTTP {response.status}: {text}"

                    # Попытка декодировать JSON
                    try:
                        data = await response.json()
                    except Exception as e:
                        logging.error(f"Ошибка декодирования JSON: {e}")
                        return f"Ошибка декодирования JSON: {e}"

            # Проверка структуры ответа
            try:
                assistant_reply = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                logging.error(f"Неправильная структура ответа: {e}")
                return {"Неправильная структура ответа": e, "Ответ": data}

            self.messages.append({"role": role, "content": assistant_reply})
            return assistant_reply

        except aiohttp.ClientError as e:
            logging.error(f"Ошибка сети: {e}")
            return f"Ошибка сети: {e}"
        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}")
            return f"Неизвестная ошибка: {e}"
        
    def clear_history(self):
        self.messages = []
        return {"data": "Success!"}