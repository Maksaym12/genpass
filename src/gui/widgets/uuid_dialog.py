from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QWidget, QPushButton, QRadioButton,
                           QApplication, QButtonGroup, QCheckBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor
import os
import sys
from src.utils.styles import *
from src.gui.widgets.custom_widgets import CloseButton, AnimatedButton
from src.core.uuid_generator import UUIDGenerator

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class UUIDDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = None
        self.title_bar = None
        self.uppercase = False
        
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(450, 250)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(7, 7, 7, 7)
        main_layout.setSpacing(0)
        
        content_frame = QFrame()
        content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_PRIMARY};
                border-radius: 13px;
            }}
        """)
        
        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        
        header = QWidget()
        header.setFixedHeight(40)
        header.setStyleSheet(f"""
            background-color: {DARK_PRIMARY};
            border-top-left-radius: 13px;
            border-top-right-radius: 13px;
        """)
        self.title_bar = header
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        icon_label = QLabel()
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "uuid_icon.png"))
        if os.path.exists(icon_path):
            icon_pixmap = QIcon(icon_path).pixmap(QSize(24, 24))
            icon_label.setPixmap(icon_pixmap)
            icon_label.setFixedSize(24, 24)
        
        title = QLabel("Генератор UUID v4")
        title.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: bold;
        """)
        
        close_button = CloseButton()
        close_button.clicked.connect(self.close)
        
        header_layout.addWidget(icon_label)
        header_layout.addSpacing(5)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        frame_layout.addWidget(header)
        
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(13, 7, 13, 7)
        content_layout.setSpacing(7)
        
        uuid_field_container = QWidget()
        uuid_field_container.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_SECONDARY};
                border-radius: 5px;
            }}
        """)
        
        uuid_field_layout = QHBoxLayout(uuid_field_container)
        uuid_field_layout.setContentsMargins(5, 5, 5, 5)
        uuid_field_layout.setSpacing(0)
        
        self.uuid_display = QLabel("Нажмите кнопку для генерации пароля")
        self.uuid_display.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        
        icon_button = QPushButton()
        icon_button.setFixedSize(30, 30)
        icon_button.setCursor(Qt.PointingHandCursor)
        icon_button.clicked.connect(self.copy_to_clipboard)
        icon_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {DARK_PRIMARY};
                border-radius: 15px;
            }}
        """)
        
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "copy.png"))
        if os.path.exists(icon_path):
            icon_button.setIcon(QIcon(icon_path))
            icon_button.setIconSize(QSize(24, 24))
        
        uuid_field_layout.addWidget(self.uuid_display, stretch=1)
        uuid_field_layout.addWidget(icon_button)
        
        content_layout.addWidget(uuid_field_container)
        
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(5)
        
        format_layout = QHBoxLayout()
        format_layout.setContentsMargins(0, 0, 0, 0)
        format_layout.setSpacing(10)
        
        format_label = QLabel("Формат:")
        format_label.setStyleSheet(f"color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        format_layout.addWidget(format_label)
        
        self.format_group = QButtonGroup()
        
        standard_radio = QRadioButton("Стандартный")
        standard_radio.setChecked(True)
        standard_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
            }}
            QRadioButton::indicator {{
                width: 15px;
                height: 15px;
                border-radius: 8px;
                border: 2px solid {ACCENT_COLOR};
            }}
            QRadioButton::indicator:checked {{
                background-color: {ACCENT_COLOR};
                border: 4px solid {DARK_SECONDARY};
            }}
        """)
        self.format_group.addButton(standard_radio, 0)
        format_layout.addWidget(standard_radio)
        
        hyphen_free_radio = QRadioButton("Без дефисов")
        hyphen_free_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
            }}
            QRadioButton::indicator {{
                width: 15px;
                height: 15px;
                border-radius: 8px;
                border: 2px solid {ACCENT_COLOR};
            }}
            QRadioButton::indicator:checked {{
                background-color: {ACCENT_COLOR};
                border: 4px solid {DARK_SECONDARY};
            }}
        """)
        self.format_group.addButton(hyphen_free_radio, 1)
        format_layout.addWidget(hyphen_free_radio)
        
        options_layout.addLayout(format_layout)
        
        case_check = QCheckBox("Верхний регистр")
        case_check.setStyleSheet(f"""
            QCheckBox {{
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {ACCENT_COLOR};
                border-radius: 2px;
                background-color: transparent;
            }}
            QCheckBox::indicator:checked {{
                background-color: {ACCENT_COLOR};
            }}
        """)
        case_check.stateChanged.connect(self.toggle_case)
        options_layout.addWidget(case_check)
        
        content_layout.addWidget(options_container)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        generate_button = AnimatedButton("СГЕНЕРИРОВАТЬ")
        generate_button.clicked.connect(self.generate_uuid)
        button_layout.addWidget(generate_button)
        
        content_layout.addLayout(button_layout)
        
        frame_layout.addWidget(content_container)
        main_layout.addWidget(content_frame)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.title_bar and self.title_bar.geometry().contains(event.pos()):
                self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
                QApplication.setOverrideCursor(Qt.ClosedHandCursor)
                event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()
                
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragPos is not None:
            self.dragPos = None
            QApplication.restoreOverrideCursor()
            event.accept()
            
    def toggle_case(self, state):
        self.uppercase = (state == Qt.Checked)
        
    def generate_uuid(self):
        if self.format_group.checkedId() == 0:  
            if self.uppercase:
                uuid = UUIDGenerator.generate_uppercase()
            else:
                uuid = UUIDGenerator.generate()
        else:  
            if self.uppercase:
                uuid = UUIDGenerator.generate_uppercase_hyphen_free()
            else:
                uuid = UUIDGenerator.generate_hyphen_free()
        
        self.uuid_display.setText(uuid)
        
    def copy_to_clipboard(self):
        text = self.uuid_display.text()
        if text != "Нажмите кнопку для генерации пароля":
            QApplication.clipboard().setText(text)
            original_text = text
            self.uuid_display.setText("UUID скопирован в буфер обмена")
            
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(2000, lambda: self.uuid_display.setText(original_text))
