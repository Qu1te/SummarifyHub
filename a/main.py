from flask import Flask, render_template, request, jsonify, redirect, url_for
import time
import requests
from dotenv import dotenv_values
from yandexgpt import generate_answer

config = dotenv_values(".env")
app = Flask(__name__)


def translate(text, target_language="ru"):
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {config['YANDEX_TRANSLATE_SERVICE_API_KEY']}"
    }
    data = {
        "targetLanguageCode": target_language,
        "texts": text
    }
    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    return res['translations'][0]['text']

@app.route('/ru/')
def index_ru():
    return render_template('index_ru.html')

@app.route('/kk/')
def index_kk():
    return render_template('index_kk.html')

@app.route('/en/')
def index_en():
    return render_template('index_en.html')

@app.route('/')
def index():
    return redirect(url_for('index_ru'))


@app.route('/process_text', methods=['POST'])
def process_text():
    user_input = request.form['user_input']
    a = time.time()
    translated = translate(user_input, "ru")
    answer = generate_answer(translated, config['YANDEXGPT_SERVICE_API_KEY'], config['YANDEXGPT_IDENTIFY_CATALOG'])
    
    output_ru = answer
    output_en = translate(answer, 'en')
    output_kz = translate(answer, 'kk')
    b = time.time() - a
    print(f"Прошло {b} секунд сначала обработки")
    return jsonify({"output_ru": output_ru, "output_kz": output_kz, "output_en": output_en}), 200

if __name__ == '__main__':
    app.run(debug=True)