import logging
from pynput import keyboard
import threading
import time

# 设置日志文件和格式
logging.basicConfig(filename="keyboard_log.txt", level=logging.INFO, format='%(asctime)s: %(message)s')

# 用于缓存按键记录
key_buffer = []
exit_event = threading.Event()

# 按键记录函数
def on_press(key):
    # 记录特殊退出按键，如Esc
    if key == keyboard.Key.esc:
        exit_event.set()
        # 停止监听
        return False
    try:
        # 记录按键（转换为字符串以便记录）
        key_buffer.append(str(key))
    except AttributeError:
        # 处理特殊按键
        key_buffer.append(str(key))

# 将缓存的数据写入文件并清空缓存
def write_to_file():
    while not exit_event.is_set():
        if key_buffer:
            logging.info(' '.join(key_buffer))
            key_buffer.clear()
        time.sleep(10)

# 监听键盘
def start_listener():
    print("按键监听已启动。按Esc键退出。")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print("按键监听已停止。")

def main():
    # 创建并启动定时保存的线程
    write_thread = threading.Thread(target=write_to_file, daemon=True)
    write_thread.start()

    # 开始监听键盘
    start_listener()

    write_thread.join()

if __name__ == '__main__':
    main()
