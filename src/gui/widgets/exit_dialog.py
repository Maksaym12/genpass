from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QWidget, QPushButton, QApplication)
from PyQt5.QtCore import Qt, QSettings, QSize
from PyQt5.QtGui import QIcon
import os
import sys
from src.utils.styles import *
from src.gui.widgets.custom_widgets import CloseButton

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ExitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = None
        self.title_bar = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(400, 180)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(0)
        
        main_frame = QFrame()
        main_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_PRIMARY};
                border-radius: 13px;
            }}
        """)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(13, 7, 13, 13)
        frame_layout.setSpacing(13)
        layout.addWidget(main_frame)

        title_bar = QWidget()
        self.title_bar = title_bar
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel()
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "exit_icon.png"))
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
            if os.path.exists(icon_path):
                icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        title_bar_layout.addWidget(icon_label)
        
        title = QLabel("Выход из приложения")
        title.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: bold;
            padding-left: 5px;
        """)
        title_bar_layout.addWidget(title)
        title_bar_layout.addStretch()
        
        close_button = CloseButton()
        close_button.clicked.connect(self.reject)
        
        title_bar_layout.addWidget(close_button)
        frame_layout.addWidget(title_bar)
        
        message_label = QLabel("Вы действительно хотите выйти из приложения?")
        message_label.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            padding: 10px;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(message_label)
        
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Отмена")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_COLOR};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER};
            }}
        """)
        cancel_button.clicked.connect(self.reject)
        
        exit_button = QPushButton("Выйти")
        exit_button.setCursor(Qt.PointingHandCursor)
        exit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ERROR_COLOR};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: #ff5252;
            }}
        """)
        exit_button.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(exit_button)
        
        frame_layout.addLayout(button_layout)
        
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