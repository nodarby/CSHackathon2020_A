from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import datetime
import hanaoke_main

app = Flask(__name__)
CORS(app)

@app.route("/api/v1/post_hanaoke", methods=['POST'])
def post_hanaoke():
    if request.method != 'POST':
        return make_response(jsonify({'result': 'invalid method'}), 400)

    fname = "data/" + datetime.datetime.now().strftime('%m%d%H%M%S') + ".wav"
    sound = request.files['hanauta']
    with open(f"{fname}", 'wb') as f:
        sound.save(f)

    # 佐藤くんのロジック部分を合体
    hanaoke = hanaoke_main.Hanaoke(fname,int(request.form['bpm'])) 

    response = make_response()

    response.data = open(hanaoke.Wav(), "rb").read()
  
    response.headers['Content-Disposition'] = 'attachment; filename=hanaoke.wav'

    response.mimetype = "audio/wav"
    return response


if __name__ == "__main__":
    app.run(debug=True)