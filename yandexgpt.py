import requests
import json

def generate_answer(newtext, service_api_key, yandex_identify_catalog):
    transcript = newtext
    prompt = {
        "modelUri": f"gpt://{yandex_identify_catalog}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Кратко перескажи текст"
            },
            {
                "role": "user",
                "text": transcript
            }

        ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {service_api_key}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    responsed = json.loads(response.text)
    try:
        result = responsed['result']['alternatives'][0]["message"]['text']
    except KeyError as e:
        print(f"Ошибка: {e}")
        return "Извините. Статья не найдена"
    else:
        return result