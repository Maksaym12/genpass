import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.gui.main_window import MainWindow

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def main():
    try:
        myappid = 'genpass.password.generator.1.0.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        app = QApplication(sys.argv)
        app.setApplicationName("GenPass")
        
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            app.setWindowIcon(app_icon)
        else:
            print(f"Ошибка: файл иконки не найден: {icon_path}")
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    main() 