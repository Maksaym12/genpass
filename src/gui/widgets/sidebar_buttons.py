from PyQt5.QtWidgets import QPushButton, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import os
import sys
from src.utils.styles import *
from src.gui.widgets.settings_dialog import SettingsDialog
from src.gui.widgets.about_dialog import AboutDialog
from src.gui.widgets.uuid_dialog import UUIDDialog
from PyQt5.QtCore import QSettings

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SidebarButton(QPushButton):
    def __init__(self, icon_name, tooltip, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        self.color = color
        self.hover_color = self._darken_color(color, 0.85)
        
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", icon_name))
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        else:
            self.setText(tooltip[0] if tooltip else "")
            
        self._update_stylesheet(False)
        
    def enterEvent(self, event):
        self._update_stylesheet(True)
        
    def leaveEvent(self, event):
        self._update_stylesheet(False)
        
    def _update_stylesheet(self, is_hover):
        bg_color = self.hover_color if is_hover else self.color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 5px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
                font-weight: bold;
                padding: 4px;
            }}
        """)
    
    def _darken_color(self, color, factor):
        from PyQt5.QtGui import QColor
        c = QColor(color)
        return f"rgb({int(c.red() * factor)}, {int(c.green() * factor)}, {int(c.blue() * factor)})"

class SettingsButton(SidebarButton):
    def __init__(self, parent=None):
        super().__init__("settings_icon.png", "Настройки приложения", parent)
        self.clicked.connect(self.show_settings)
        
    def show_settings(self):
        main_window = self.window()
        
        if main_window and hasattr(main_window, "open_settings"):
            main_window.open_settings()
        else:
            dialog = SettingsDialog(self.window())
            dialog.setWindowTitle("Настройки приложения")
            dialog.setWindowModality(Qt.ApplicationModal)
            
            if main_window:
                dialog.tray_setting_changed.connect(main_window.update_tray_icon)
            
            if dialog.exec_() == SettingsDialog.Accepted:
                if main_window:
                    settings = QSettings("GenPass", "PasswordGenerator")
                    main_window.default_length = settings.value("default_length", 12, type=int)
                    
                    main_window.length_slider.setValue(main_window.default_length)
                    
                    for child in main_window.findChildren(QLabel):
                        if "Длина пароля:" in child.text():
                            child.setText(f"Длина пароля: {main_window.default_length} символов (по умолчанию)")
                            break

class AboutButton(SidebarButton):
    def __init__(self, parent=None):
        super().__init__("info_icon.png", "О программе", parent)
        self.clicked.connect(self.show_about)
        
    def show_about(self):
        dialog = AboutDialog(self.window())
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

class UUIDButton(SidebarButton):
    def __init__(self, parent=None):
        super().__init__("uuid_icon.png", "UUID Генератор", parent)
        self.clicked.connect(self.show_uuid_generator)
        
    def show_uuid_generator(self):
        dialog = UUIDDialog(self.window())
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()
