# app.py
import os
from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# --- ここにAzureの情報を入力してください ---
AZURE_PREDICTION_URL = os.environ.get("https://myqnabot-language.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=WebApp-KB&api-version=2021-10-01&deploymentName=production")
AZURE_SUBSCRIPTION_KEY = os.environ.get("9WBMBb6ASECgzqz9zlleP2InlYLfDkuuw7zxceFDcP32UrTFmCSbJQQJ99BGACxCCsyXJ3w3AAAaACOGC3Qg")


# -----------------------------------------

# ユーザーが最初のページにアクセスしたときに表示する処理
@app.route('/')
def index():
    return render_template('index.html')  # index.htmlという画面を表示する


# '/ask' というアドレスにデータが送られてきたときの処理
@app.route('/ask', methods=['POST'])
def ask_question():
    # ユーザーが入力した質問データを取り出す
    data = request.get_json()
    user_question = data['question']

    # Azure AIに送るためのデータ形式を整える
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "question": user_question
    }

    # Azure AIに質問を送信し、答えをもらう
    try:
        response = requests.post(AZURE_PREDICTION_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        answer_data = response.json()

        # 答えが見つかった場合
        if answer_data['answers']:
            answer = answer_data['answers'][0]['answer']
        # 答えが見つからなかった場合
        else:
            answer = "すみません、その質問にはお答えできません。"

        # 答えを画面に返す
        return jsonify({'answer': answer})

    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({'error': 'AIとの通信中にエラーが発生しました。'}), 500


# このプログラムを実行したときにサーバーを起動する
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)