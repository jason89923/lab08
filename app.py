from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# 摩斯密码处理相关参数
BUTTON_PRESSED = False
PRESS_TIME = None
RELEASE_TIME = None
MORSE_BUFFER = []
MAX_MORSE_LENGTH = 6

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
