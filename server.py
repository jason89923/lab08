from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask import request, jsonify

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    # 首頁
    return render_template('index.html')

# 處理Socket
@socketio.on('connect')
def handle_connect():
    print('Socket connected.')
    emit('message', {'data': '已连接到服务器'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Socket closed.')

# @socketio.on('morse_input')
# def handle_morse_input(data):
#     code = data.get('code', '')
#     decoded_char = morse_code_map.get(code, 'invalid code')
#     emit('decoded_char', {'code': code, 'char': decoded_char})
    
@app.route('/morse', methods=['POST'])
def handle_post():
    # code decode
    data = request.get_json()
    print(data)
    socketio.emit('decoded_char', data)
    return jsonify({'status': 'success'})

def main():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
