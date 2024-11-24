import socket
import time

# 設定伺服器參數
HOST = '0.0.0.0'
PORT = 8080

# 摩斯密碼處理相關參數
BUTTON_PRESSED = False
PRESS_TIME = None
RELEASE_TIME = None
MORSE_BUFFER = []
MAX_MORSE_LENGTH = 6

def clear_morse():
    """清空摩斯密碼緩衝區"""
    global MORSE_BUFFER
    MORSE_BUFFER = []

def parse_morse_code(morse_buffer):
    """解析摩斯密碼"""
    morse_str = ''.join(morse_buffer)
    morse_dict = {
        "-.-.": 'C',
        ".": 'E',
        "..": 'I',
        "-.--": 'Y'
    }
    return morse_dict.get(morse_str, None)

def handle_button_event(state):
    """處理按鈕事件"""
    global BUTTON_PRESSED, PRESS_TIME, RELEASE_TIME, MORSE_BUFFER

    if state == '1' and not BUTTON_PRESSED:  # 按鈕被按下
        BUTTON_PRESSED = True
        PRESS_TIME = time.time()
    elif state == '0' and BUTTON_PRESSED:  # 按鈕被釋放
        BUTTON_PRESSED = False
        RELEASE_TIME = time.time()

        # 計算按下的持續時間
        duration = (RELEASE_TIME - PRESS_TIME) * 1000  # 轉換為毫秒
        if duration < 200:
            MORSE_BUFFER.append('.')
            print('.', end='', flush=True)  # 短按 (dot)
        else:
            MORSE_BUFFER.append('-')
            print('-', end='', flush=True)  # 長按 (dash)

def check_morse_idle():
    """檢查是否有長時間無輸入並處理摩斯密碼"""
    global RELEASE_TIME, BUTTON_PRESSED, MORSE_BUFFER

    if RELEASE_TIME:
        idle_duration = (time.time() - RELEASE_TIME) * 1000
        if not BUTTON_PRESSED and idle_duration > 500 and MORSE_BUFFER:
            result = parse_morse_code(MORSE_BUFFER)
            if result:
                print(f" -> {result}")
            else:
                print("\nInvalid Morse code sequence.")
            clear_morse()


def start_server():
    """啟動Socket伺服器（非阻塞模式）"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允許地址重用
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        conn.setblocking(False)  # 設定為非阻塞模式
        print(f"Connection established with {addr}.")

        while True:
            try:
                data = conn.recv(2)
                if not data:  # 檢查連接是否已關閉
                    print("Connection closed by client.")
                    break

                state = data.decode().strip().rstrip('\x00')  # 去除尾部多餘字元
                if state in {'0', '1'}:
                    handle_button_event(state)  # 處理按鈕事件
                else:
                    print(f"Unexpected data received: {state}")
            except BlockingIOError:
                # 如果沒有資料可讀，這裡不阻塞，繼續執行其他操作
                check_morse_idle()  # 檢查摩斯密碼的閒置時間處理
                time.sleep(0.1)  # 避免無限快速循環浪費CPU
            except Exception as e:
                print(f"An error occurred: {e}")
                break

def main():
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
