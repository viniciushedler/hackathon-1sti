import sys

import datetime
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/', methods = ['GET', 'POST'])
def render_app_template():
    return render_template('index.html')

@app.route('/upload_webcam_file', methods = ['POST'])
def upload_webcam_file():
    print("request received")
    
    file = request.files['image']

    print("\n"*10)
    print(file)
    print("\n"*10)

    resp = {'success': True, 'response': 'Arquivo salvo com sucesso'}

    return jsonify(resp), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
