from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QWidget, QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
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

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = None
        self.title_bar = None
        self.setup_ui()
        
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
        
    def setup_ui(self):
        self.setFixedSize(450, 350)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(0)
        
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_PRIMARY};
                border-radius: 13px;
            }}
        """)
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title bar
        title_bar = QWidget()
        self.title_bar = title_bar
        title_bar.setCursor(Qt.ArrowCursor)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 7, 20, 0)
        title_layout.setSpacing(5)
        
        icon = QLabel()
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
        if os.path.exists(icon_path):
            icon.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            print(f"Ошибка: файл иконки не найден: {icon_path}")
        
        title = QLabel("О программе")
        title.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: bold;
        """)
        
        close_button = CloseButton()
        close_button.clicked.connect(self.close)
        
        title_layout.addWidget(icon)
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(close_button)
        
        # Content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 15, 20, 20)
        content_layout.setSpacing(15)
        
        logo_container = QHBoxLayout()
        logo = QLabel()
        logo_path = get_resource_path(os.path.join("src", "assets", "icons", "password_generator.png"))
        if os.path.exists(logo_path):
            logo_pixmap = QIcon(logo_path).pixmap(64, 64)
            logo.setPixmap(logo_pixmap)
        else:
            print(f"Ошибка: файл логотипа не найден: {logo_path}")
        logo.setAlignment(Qt.AlignCenter)
        logo_container.addStretch()
        logo_container.addWidget(logo)
        logo_container.addStretch()
        
        version = QLabel("GenPass v.1.0.4")
        version.setStyleSheet(f"""
            color: {WARNING_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: bold;
        """)
        version.setAlignment(Qt.AlignCenter)
        
        description = QLabel("Генератор надежных паролей")
        description.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
        """)
        description.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("с расчетом криптостойкости")
        subtitle.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
            font-style: italic;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        dev_container = QHBoxLayout()
        dev_container.setContentsMargins(0, 10, 0, 0)
        
        dev_info = QLabel("Разработчик:")
        dev_info.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
        """)
        
        dev_name = QLabel("Макс Лейбер")
        dev_name.setStyleSheet(f"""
            color: {WARNING_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            font-weight: bold;
        """)
        
        dev_container.addStretch()
        dev_container.addWidget(dev_info)
        dev_container.addWidget(dev_name)
        dev_container.addStretch()
        
        github_button = QPushButton("github.com/MaksymLeiber")
        github_button.setCursor(Qt.PointingHandCursor)
        github_button.setStyleSheet(f"""
            QPushButton {{
                color: {ACCENT_COLOR};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_SMALL}px;
                border: none;
                background: transparent;
                text-decoration: underline;
            }}
            QPushButton:hover {{
                color: {ACCENT_HOVER};
            }}
        """)
        github_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/MaksymLeiber")))
        github_button.setFixedHeight(20)
        
        bottom_container = QHBoxLayout()
        bottom_container.setContentsMargins(0, 10, 0, 0)
        
        license_info = QLabel("MIT License")
        license_info.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
        """)
        
        copyright = QLabel("© 2025")
        copyright.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
        """)
        
        bottom_container.addWidget(license_info)
        bottom_container.addStretch()
        bottom_container.addWidget(copyright)
        
        content_layout.addLayout(logo_container)
        content_layout.addWidget(version)
        content_layout.addWidget(description)
        content_layout.addWidget(subtitle)
        content_layout.addLayout(dev_container)
        content_layout.addWidget(github_button)
        content_layout.addStretch()
        content_layout.addLayout(bottom_container)
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)
        layout.addWidget(container) 