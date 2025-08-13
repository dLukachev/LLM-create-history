import os
import aiohttp
from dotenv import load_dotenv
import json
import logging

from utils.redis import redis_client

load_dotenv()

MODEL = os.getenv('MODEL')
KEY = os.getenv('OPENROUTER_KEY')
URL = os.getenv('URL_ROUTER')

class OpenRouterService:

    def __init__(self, api_key=KEY, model=MODEL, url=URL) -> None:
        self.api_key = api_key
        self.model = model
        self.url = url

    async def call(self, prompt, role="user", session_id=None):
        message = []

        if session_id:
            cache = await redis_client.get(f"session:{session_id}")
            messages = json.loads(cache) if cache else []

        message.append({"role": role, "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": role, "content": prompt}]
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
            
            if session_id:
                messages.append({"role": role, "content": json.dumps(assistant_reply)}) # type: ignore
                await redis_client.set(f"session:{session_id}", json.dumps(messages), ex=3600) # type: ignore
                await redis_client.close() # type: ignore

            return assistant_reply

        except aiohttp.ClientError as e:
            logging.error(f"Ошибка сети: {e}")
            return f"Ошибка сети: {e}"
        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}")
            return f"Неизвестная ошибка: {e}"