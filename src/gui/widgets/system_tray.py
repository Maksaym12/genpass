from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import sys
from src.utils.styles import *

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SystemTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        
        self.setup_menu()
        
        self.activated.connect(self.on_tray_icon_activated)
        
    def setup_menu(self):
        menu = QMenu(self.parent)
        
        show_action = QAction("Открыть", self.parent)
        show_action.triggered.connect(self.parent.show)
        
        exit_action = QAction("Выход", self.parent)
        exit_action.triggered.connect(self.parent.close)
        
        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        
        self.setContextMenu(menu)
        
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.parent.isHidden():
                self.parent.show()
                self.parent.activateWindow()
            else:
                self.parent.hide()
                
    def show_message(self, title, message, icon=QSystemTrayIcon.Information, timeout=3000):
        self.showMessage(title, message, icon, timeout) 