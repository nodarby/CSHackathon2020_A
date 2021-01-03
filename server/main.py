from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route("/api/v1/post_hanaoke", methods=['POST'])
def post_hanaoke():
    if request.method != 'POST':
        return make_response(jsonify({'result': 'invalid method'}), 400)

    #録音した音声のバイナリデータ
    fname = "sounds/" + datetime.datetime.now().strftime('%m%d%H%M%S') + ".wav"
    with open(f"{fname}", 'wb') as f:
        f.write(request.files['hanauta'].read())
    print(f"posted sound file: {fname}")
    # 佐藤くんのロジック部分を合体
    print("BPM:"+request.form['bpm'])

    # 生成した音声データを返す
    return "hello"


if __name__ == "__main__":
    app.run(debug=True)