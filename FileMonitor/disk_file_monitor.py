import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 监控的源硬盘路径
source_drive = "C:\\"

# 目标文件夹路径
destination_folder = "D:\\NewFiles\\"

# 创建目标文件夹（如果不存在）
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 是否启用详细输出
verbose = True

# 系统文件夹列表
system_folders = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData",
    "C:\\Users\\Public",
    "C:\\System Volume Information",
    "C:\\Users\\jiawe\AppData"
]

# 文件事件处理程序
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(destination_folder, file_name)

            # 检查文件是否在系统文件夹中
            is_system_file = False
            for folder in system_folders:
                if file_path.startswith(folder):
                    is_system_file = True
                    break

            if not is_system_file:
                # 检查源文件是否存在
                if os.path.exists(file_path):
                    try:
                        shutil.copy2(file_path, destination_path)
                        if verbose:
                            print(f"复制文件: {file_path} -> {destination_path}")
                        else:
                            print(f"复制文件: {file_name}")
                    except (FileNotFoundError, PermissionError) as e:
                        print(f"复制文件时出错: {file_path}")
                        print(f"错误信息: {str(e)}")
                else:
                    print(f"源文件不存在: {file_path}")

# 创建文件系统观察器
observer = Observer()
event_handler = FileEventHandler()
observer.schedule(event_handler, source_drive, recursive=True)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()