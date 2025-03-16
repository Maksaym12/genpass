from PyQt5.QtWidgets import (QPushButton, QDialog, QVBoxLayout, 
                           QLabel, QFrame, QScrollArea, QWidget, QHBoxLayout, QApplication)
from PyQt5.QtCore import Qt
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

class HelpButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
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
        self.setText("?")
        self.clicked.disconnect() if self.receivers(self.clicked) > 0 else None
        self.clicked.connect(lambda: self.show_help())
        
    def show_help(self):
        dialog = HelpDialog(self.window())
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.show()

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        flags = Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 500)
        self.dragPos = None
        self.title_bar = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        main_frame = QFrame(self)
        main_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_PRIMARY};
                border-radius: 13px;
            }}
        """)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(20, 7, 20, 20)
        frame_layout.setSpacing(13)
        layout.addWidget(main_frame)

        title_bar = QWidget()
        self.title_bar = title_bar
        title_bar.setCursor(Qt.ArrowCursor)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel()
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            print(f"Ошибка: файл иконки не найден: {icon_path}")
        title_bar_layout.addWidget(icon_label)
        
        title = QLabel("Почему важен надежный пароль?")
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
        
        help_text = [
            ("1. Защита от взлома",
             "Сложные пароли значительно труднее подобрать методом перебора или угадать. Современные компьютеры способны перебирать миллионы комбинаций в секунду, поэтому простые пароли могут быть взломаны за считанные минуты. Используя сложный пароль, вы увеличиваете время, необходимое для его взлома, с нескольких минут до сотен или тысяч лет."),
            
            ("2. Разные типы символов",
             "Использование букв, цифр и специальных символов увеличивает количество возможных комбинаций в миллионы раз. Например, пароль только из строчных букв (26 символов) длиной 8 символов имеет 208 миллиардов комбинаций. Добавив заглавные буквы, цифры и специальные символы (всего около 95 символов), количество комбинаций возрастает до 6.6 квадриллионов!"),
            
            ("3. Длина пароля",
             "Чем длиннее пароль, тем больше времени потребуется для его взлома. Рекомендуемая длина - от 12 символов. Каждый дополнительный символ экспоненциально увеличивает сложность пароля. Пароль длиной 12 символов, содержащий все типы символов, потребует миллионы лет для взлома даже на мощном компьютере."),
            
            ("4. Уникальность",
             "Использование уникальных паролей для разных сервисов защищает все ваши аккаунты, даже если один из них будет скомпрометирован. Если вы используете один и тот же пароль везде, взлом одного аккаунта приведет к компрометации всех остальных. Рекомендуется использовать разные пароли для: банковских приложений, электронной почты, социальных сетей и других важных сервисов."),
            
            ("5. Автоматическая генерация",
             "Генератор создает действительно случайные пароли, которые невозможно предугадать, в отличие от паролей, придуманных человеком. Люди часто используют предсказуемые шаблоны: даты рождения, имена, простые замены букв на цифры (например, 'password123', 'P@ssw0rd'). Автоматически сгенерированные пароли лишены этих недостатков и гарантируют максимальную случайность."),
            
            ("6. Регулярная смена",
             "Периодическая смена паролей снижает риск несанкционированного доступа к вашим данным. Даже если ваш пароль попал в руки злоумышленников, регулярная смена делает эту информацию бесполезной. Рекомендуется менять пароли каждые 3-6 месяцев, а также немедленно после любых подозрительных действий в ваших аккаунтах."),
            
            ("7. Конфиденциальность",
             "Надежный пароль - это ваш цифровой ключ, который защищает личную информацию, финансовые данные и онлайн-идентичность. В современном мире утечка пароля может привести к серьезным последствиям: краже денег с банковских счетов, потере доступа к важным сервисам, краже личных данных и документов."),
            
            ("8. Двухфакторная аутентификация",
             "Даже самый сложный пароль лучше дополнить вторым фактором защиты. Двухфакторная аутентификация (2FA) требует подтверждения входа через второе устройство (например, телефон) или биометрические данные. Это значительно усложняет взлом аккаунта, даже если пароль стал известен злоумышленникам."),
            
            ("9. Безопасное хранение",
             "Никогда не записывайте пароли на бумаге или в текстовом файле на компьютере. Используйте специальные менеджеры паролей с шифрованием. Они позволяют безопасно хранить все ваши пароли под защитой одного мастер-пароля и автоматически генерировать новые сложные пароли когда это необходимо."),
            
            ("10. Признаки надежного пароля",
             "• Длина не менее 12 символов\n• Комбинация строчных и заглавных букв\n• Цифры и специальные символы\n• Отсутствие личной информации\n• Отсутствие словарных слов\n• Уникальность для каждого сервиса")
        ]
        
        for title, description in help_text:
            item_container = QFrame()
            item_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {DARK_SECONDARY};
                    border-radius: 7px;
                    margin-bottom: 5px;
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
        
        content_layout.addStretch()
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