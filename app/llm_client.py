import requests
from app.config import YANDEX_API_KEY, FOLDER_ID

YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
MODEL_URI = f"gpt://{FOLDER_ID}/yandexgpt-lite"


async def generate_response(message: str) -> str:
    try:
        # Запрос к API Яндекс GPT
        resp = requests.post(
            url=YANDEX_GPT_URL,
            headers={
                "Authorization": f"Api-Key {YANDEX_API_KEY}",
                "x-folder-id": FOLDER_ID
            },
            json={
                "modelUri": MODEL_URI,
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": "2000"
                },
                "messages": [
                    {
                        "role": "system",
                        "text": message
                    }
                ]
            }
        )

        # Проверка статуса запроса
        if resp.status_code != 200:
            print(f"Ошибка: {resp.status_code}, текст ошибки: {resp.text}")
            return "Произошла ошибка при подключении к Яндекс GPT."

        # Отладка ответа от API
        print("Ответ от API:", resp.json())

        answer = resp.json()

        # Проверка наличия ключа 'result'
        if 'result' not in answer:
            return "Ответ от API не содержит поля 'result'."

        # Извлекаем ответ
        reply_text = answer['result']['alternatives'][0]['message']['text']
        return reply_text

    except Exception as e:
        print(f"Ошибка при генерации ответа: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."
