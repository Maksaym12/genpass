from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QWidget, QApplication,
                             QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon
import os
import sys
import hashlib
import random
import string
from src.utils.styles import *
from src.gui.widgets.custom_widgets import CloseButton

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = "."
    return os.path.join(base_path, relative_path)

class MasterPasswordHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = None
        self.title_bar = None
        self.setup_ui()
        
    def setup_ui(self):
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
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            print(f"Ошибка: файл иконки не найден: {icon_path}")
        title_bar_layout.addWidget(icon_label)
        
        title = QLabel("Как работает генерация по мастер-паролю?")
        title.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: bold;
            padding-left: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        close_button = CloseButton()
        close_button.clicked.connect(self.close)
        
        title_bar_layout.addWidget(title)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)
        
        frame_layout.addWidget(title_bar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {DARK_SECONDARY};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {BUTTON_COLOR};
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_PRIMARY};
            }}
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(7)
        
        help_text = [
            ("1. Что такое мастер-пароль?",
             "Мастер-пароль - это ваш основной пароль, который используется для генерации других паролей. Он должен быть надежным и легко запоминающимся для вас. Например: 'МойЛюбимыйПарольДляВсех2024!'"),
            
            ("2. Что такое домен?",
             "Домен - это название сайта или сервиса, для которого вы хотите сгенерировать пароль. Например: 'google', 'facebook', 'twitter'. Важно использовать одинаковое название домена при повторной генерации пароля."),
            
            ("3. Как работает генерация?",
             "1. Мы объединяем ваш мастер-пароль и домен\n2. Создаем уникальный хеш SHA-256\n3. Берем первые 8 символов из хеша\n4. Добавляем специальный символ (!@#)\n5. Добавляем случайную цифру\n6. Добавляем 2 заглавные буквы\n\nПример:\nМастер-пароль: MyPassword123\nДомен: google\nРезультат: 8f4e2a1b!3KL"),
            
            ("4. Преимущества этого метода",
             "• Безопасность: все вычисления происходят локально на вашем устройстве\n• Повторяемость: одинаковые мастер-пароль и домен всегда дают одинаковый результат\n• Уникальность: каждый сайт получает свой уникальный пароль\n• Надежность: генерируются сложные пароли, соответствующие требованиям безопасности"),
            
            ("5. Важные рекомендации",
             "• Никогда не используйте простые мастер-пароли\n• Запомните или надежно сохраните свой мастер-пароль\n• Используйте точные названия доменов\n• Регулярно меняйте мастер-пароль\n• Не сообщайте никому свой мастер-пароль")
        ]
        
        for title, description in help_text:
            item_container = QFrame()
            item_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {DARK_SECONDARY};
                    border-radius: 7px;
                }}
            """)
            item_layout = QVBoxLayout(item_container)
            item_layout.setContentsMargins(10, 10, 10, 10)
            item_layout.setSpacing(5)
            
            title_label = QLabel(title)
            title_label.setStyleSheet(f"""
                color: {WARNING_COLOR};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
                font-weight: bold;
            """)
            item_layout.addWidget(title_label)
            
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(f"""
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
            """)
            item_layout.addWidget(desc_label)
            
            content_layout.addWidget(item_container)
        
        scroll.setWidget(content_widget)
        frame_layout.addWidget(scroll)
        
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

class MasterPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 440)  # Уменьшил высоту окна
        self.dragPos = None
        self.title_bar = None
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(0)
        
        # Основная рамка
        main_frame = QWidget()
        main_frame.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_PRIMARY};
                border-radius: 13px;
            }}
        """)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(20, 15, 20, 20)
        frame_layout.setSpacing(20)
        
        # Заголовок
        title_bar = QWidget()
        self.title_bar = title_bar
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel()
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            print(f"Ошибка: файл иконки не найден: {icon_path}")
        title_layout.addWidget(icon_label)
        
        title = QLabel("Генерация по мастер-паролю")
        title.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_TITLE}px;
            font-weight: bold;
            padding-left: 5px;
        """)
        
        help_button = QPushButton("?")
        help_button.setFixedSize(20, 20)
        help_button.setCursor(Qt.PointingHandCursor)
        help_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {WARNING_COLOR};
                border: none;
                border-radius: 10px;
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {WARNING_HOVER};
            }}
        """)
        help_button.clicked.connect(lambda: MasterPasswordHelpDialog(self).exec_())
        
        close_button = CloseButton()
        close_button.clicked.connect(self.close)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(help_button)
        title_layout.addWidget(close_button)
        
        frame_layout.addWidget(title_bar)
        
        # Поле для мастер-пароля
        master_label = QLabel("Мастер-пароль:")
        master_label.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        frame_layout.addWidget(master_label)
        
        # Контейнер для поля ввода и кнопки показа пароля
        master_container = QWidget()
        master_layout = QHBoxLayout(master_container)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)
        
        self.master_input = QLineEdit()
        self.master_input.setFixedHeight(45)
        self.master_input.setEchoMode(QLineEdit.Password)
        self.master_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 7px;
                border-top-right-radius: 0;
                border-bottom-right-radius: 0;
                padding: 7px 15px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
            }}
        """)
        
        # Кнопка показа пароля
        show_password_button = QPushButton()
        show_password_button.setFixedSize(45, 45)
        show_password_button.setCursor(Qt.PointingHandCursor)
        show_password_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_SECONDARY};
                border: none;
                border-radius: 7px;
                border-top-left-radius: 0;
                border-bottom-left-radius: 0;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_COLOR};
            }}
        """)
        
        # Иконка для кнопки показа пароля
        eye_icon_path = get_resource_path(os.path.join("src", "assets", "icons", "eye.png"))
        if os.path.exists(eye_icon_path):
            show_password_button.setIcon(QIcon(eye_icon_path))
            show_password_button.setIconSize(QSize(22, 22))
        
        # Обработчик нажатия на кнопку показа пароля
        def toggle_password_visibility():
            if self.master_input.echoMode() == QLineEdit.Password:
                self.master_input.setEchoMode(QLineEdit.Normal)
            else:
                self.master_input.setEchoMode(QLineEdit.Password)
        
        show_password_button.clicked.connect(toggle_password_visibility)
        
        master_layout.addWidget(self.master_input, stretch=1)
        master_layout.addWidget(show_password_button)
        
        frame_layout.addWidget(master_container)
        
        # Поле для домена
        domain_label = QLabel("Домен (например, google, binance, etc.):")
        domain_label.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        frame_layout.addWidget(domain_label)
        
        self.domain_input = QLineEdit()
        self.domain_input.setFixedHeight(45)
        self.domain_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 7px;
                padding: 7px 15px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
            }}
        """)
        frame_layout.addWidget(self.domain_input)
        
        # Результат
        result_container = QWidget()
        result_layout = QHBoxLayout(result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(0)
        
        self.result_label = QLabel("Здесь появится сгенерированный пароль")
        self.result_label.setStyleSheet(f"""
            QLabel {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                padding: 7px;
                border-radius: 7px;
                border-top-right-radius: 0;
                border-bottom-right-radius: 0;
                font-family: {FONT_FAMILY};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        self.result_label.setAlignment(Qt.AlignCenter)
        
        # Кнопка копирования
        copy_button = QPushButton()
        copy_button.setFixedSize(50, 52)
        copy_button.setCursor(Qt.PointingHandCursor)
        copy_button.clicked.connect(self.copy_to_clipboard)
        copy_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_SECONDARY};
                border: none;
                border-radius: 7px;
                border-top-left-radius: 0;
                border-bottom-left-radius: 0;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_COLOR};
            }}
        """)
        
        # Иконка копирования
        copy_icon_path = get_resource_path(os.path.join("src", "assets", "icons", "copy.png"))
        if os.path.exists(copy_icon_path):
            copy_button.setIcon(QIcon(copy_icon_path))
            copy_button.setIconSize(QSize(20, 20))
        
        result_layout.addWidget(self.result_label, stretch=1)
        result_layout.addWidget(copy_button)
        
        frame_layout.addWidget(result_container)
        
        # Кнопка генерации
        generate_button = QPushButton("СГЕНЕРИРОВАТЬ")
        generate_button.setCursor(Qt.PointingHandCursor)
        generate_button.clicked.connect(self.generate_password)
        generate_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_COLOR};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 7px;
                padding: 10px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
            }}
            QPushButton:hover {{
                background-color: {BUTTON_HOVER};
            }}
        """)
        frame_layout.addWidget(generate_button)
        
        layout.addWidget(main_frame)
        
    def generate_password(self):
        master = self.master_input.text()
        domain = self.domain_input.text()
        
        if not master or not domain:
            self.result_label.setText("Введите мастер-пароль и домен")
            return
            
        # Комбинируем мастер-пароль и домен
        combined = f"{master}:{domain}"
        # Создаем SHA-256 хеш
        hash_object = hashlib.sha256(combined.encode())
        hash_hex = hash_object.hexdigest()
        
        # Берем первые 12 символов и добавляем специальные символы
        password = hash_hex[:8]
        password += "!@#"[hash_hex.count('a') % 3]  # Добавляем спецсимвол
        password += str(hash_hex.count('e') % 10)   # Добавляем цифру
        password += hash_hex[8:10].upper()          # Добавляем заглавные буквы
        
        self.result_label.setText(f"Ваш пароль: {password}")
        
    def copy_to_clipboard(self):
        text = self.result_label.text()
        if text.startswith("Ваш пароль: "):
            password = text.replace("Ваш пароль: ", "")
            QApplication.clipboard().setText(password)
            original_text = self.result_label.text()
            self.result_label.setText("Пароль скопирован в буфер обмена")
            QTimer.singleShot(2000, lambda: self.result_label.setText(original_text))
            
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