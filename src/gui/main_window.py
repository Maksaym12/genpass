from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame, QApplication, QPushButton)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon
import os
import sys
from src.utils.styles import *
from src.gui.widgets.custom_widgets import AnimatedToggle, CustomSlider, AnimatedButton, CloseButton, MinimizeButton
from src.gui.widgets.help_dialog import HelpButton, HelpDialog
from src.gui.widgets.about_dialog import AboutDialog
from src.gui.widgets.combination_calculator import CombinationCalculator
from src.gui.widgets.master_password_dialog import MasterPasswordDialog
from src.core.password_generator import PasswordGenerator

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = "."
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.password_generator = PasswordGenerator()
        self.dragPos = None
        self.strength_label = QLabel("Примерная сложность: 0%")
        self.title_bar = None
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self._update_typewriter)
        self.current_password = ""
        self.current_index = 0
        self.initUI()
        
    def update_strength_indicator(self):

        length = self.length_slider.value()
        use_upper = self.toggles['upper']._enabled
        use_lower = self.toggles['lower']._enabled
        use_digits = self.toggles['digits']._enabled
        use_special = self.toggles['special']._enabled
        
        self.combination_calculator.update_combinations(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_special=use_special
        )
        
        if not any([use_upper, use_lower, use_digits, use_special]):
            strength = 0
            self.strength_label.setText("Сложность: 0%")
        else:
            test_password = ""
            if use_upper:
                test_password += "A"
            if use_lower:
                test_password += "a"
            if use_digits:
                test_password += "1"
            if use_special:
                test_password += "!"
            
            remaining_length = length - len(test_password)
            if remaining_length > 0:
                if use_upper:
                    test_password += "A" * remaining_length
                elif use_lower:
                    test_password += "a" * remaining_length
                elif use_digits:
                    test_password += "1" * remaining_length
                elif use_special:
                    test_password += "!" * remaining_length
            
            strength = self.password_generator.check_strength(test_password)
            
            self.strength_label.setText(f"Примерная сложность: {strength}%")
        
        if strength >= 75:
            color = SUCCESS_COLOR
        elif strength >= 50:
            color = WARNING_COLOR
        else:
            color = ERROR_COLOR
            
        self.strength_label.setStyleSheet(f"""
            color: {color};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
        """)

    def initUI(self):
        try:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
            
            icon_path = get_resource_path(os.path.join("src", "assets", "icons", "pass_logo.png"))
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                print(f"Ошибка: файл иконки не найден: {icon_path}")
            
            main_widget = QWidget()
            self.setCentralWidget(main_widget)
            layout = QVBoxLayout(main_widget)
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
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
            title_bar_layout.addWidget(icon_label)
            
            title = QLabel("GenPass")
            title.setStyleSheet(f"""
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_TITLE}px;
                font-weight: bold;
                padding-left: 5px;
            """)
            title_bar_layout.addWidget(title)
            title_bar_layout.addStretch()
            
            help_button = HelpButton()
            info_button = QPushButton("i")
            info_button.setFixedSize(20, 20)
            info_button.setCursor(Qt.PointingHandCursor)
            info_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ACCENT_COLOR};
                    color: {TEXT_COLOR};
                    border: none;
                    border-radius: 10px;
                    font-family: {FONT_FAMILY};
                    font-size: {FONT_SIZE_NORMAL}px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {ACCENT_HOVER};
                }}
            """)
            info_button.clicked.connect(lambda: AboutDialog(self).exec_())
            
            minimize_button = MinimizeButton()
            minimize_button.clicked.connect(self.showMinimized)
            close_button = CloseButton()
            close_button.clicked.connect(self.close)
            
            title_bar_layout.addWidget(help_button)
            title_bar_layout.addWidget(info_button)
            title_bar_layout.addWidget(minimize_button)
            title_bar_layout.addWidget(close_button)
            
            frame_layout.addWidget(title_bar)
            
            password_container = QWidget()
            password_layout = QHBoxLayout(password_container)
            password_layout.setContentsMargins(0, 0, 0, 0)
            password_layout.setSpacing(0)
            
            self.password_field = QLabel("Нажмите кнопку для генерации пароля")
            self.password_field.setStyleSheet(f"""
                QLabel {{
                    background-color: {DARK_SECONDARY};
                    color: {TEXT_COLOR};
                    padding: 7px;
                    border-radius: 7px;
                    border-top-right-radius: 0;
                    border-bottom-right-radius: 0;
                    font-family: {FONT_FAMILY};
                    font-size: 13px;
                    font-weight: 600;
                }}
            """)
            self.password_field.setAlignment(Qt.AlignCenter)
            
            copy_button_field = QPushButton()
            copy_button_field.setFixedSize(50, 52) 
            copy_button_field.setCursor(Qt.PointingHandCursor)
            copy_button_field.clicked.connect(self.copy_to_clipboard)
            copy_button_field.setStyleSheet(f"""
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
            
            copy_icon_path = get_resource_path(os.path.join("src", "assets", "icons", "copy.png"))
            if os.path.exists(copy_icon_path):
                copy_button_field.setIcon(QIcon(copy_icon_path))
                copy_button_field.setIconSize(QSize(20, 20))
            else:
                print(f"Ошибка: файл иконки копирования не найден: {copy_icon_path}")
            
            password_layout.addWidget(self.password_field, stretch=1)
            password_layout.addWidget(copy_button_field)
            
            frame_layout.addWidget(password_container)
            
            length_label = QLabel("Длина пароля: 8 символов (по умолчанию)")
            length_label.setStyleSheet(f"color: {TEXT_COLOR}; font-size: {FONT_SIZE_NORMAL}px;")
            frame_layout.addWidget(length_label)
            
            self.length_slider = CustomSlider()
            self.length_slider.setRange(6, 32)
            self.length_slider.setValue(8)
            self.length_slider.valueChanged.connect(
                lambda v: (length_label.setText(f"Длина пароля: {v} символов"), self.update_strength_indicator())
            )
            frame_layout.addWidget(self.length_slider)
            
            self.toggles = {}
            toggle_labels = {
                'upper': 'A-Z (прописные)',
                'lower': 'a-z (строчные)',
                'digits': '0-9 (цифры)',
                'special': '!@# (символы)'
            }
            
            for key, label in toggle_labels.items():
                toggle_layout = QHBoxLayout()
                toggle = AnimatedToggle()
                toggle._enabled = True
                toggle.circle_position = TOGGLE_WIDTH - 24
                
                original_press_event = toggle.mousePressEvent
                toggle.mousePressEvent = lambda event, t=toggle, orig=original_press_event: self._handle_toggle_click(event, t, orig)
                
                label_widget = QLabel(label)
                label_widget.setStyleSheet(f"""
                    color: {TEXT_COLOR};
                    font-family: {FONT_FAMILY};
                    font-size: {FONT_SIZE_NORMAL}px;
                """)
                
                toggle_layout.addWidget(label_widget)
                toggle_layout.addWidget(toggle)
                frame_layout.addLayout(toggle_layout)
                self.toggles[key] = toggle
                
            button_layout = QHBoxLayout()
            button_layout.setSpacing(7)
            
            create_button = AnimatedButton("СОЗДАТЬ")
            create_button.clicked.connect(self.generate_password)
            
            master_button = AnimatedButton("МАСТЕР-ПАРОЛЬ")
            master_button.clicked.connect(self.show_master_dialog)
            master_button.setCursor(Qt.PointingHandCursor)
            
            create_icon_path = get_resource_path(os.path.join("src", "assets", "icons", "create_btn.png"))
            if os.path.exists(create_icon_path):
                create_button.setIcon(QIcon(create_icon_path))
                create_button.setIconSize(QSize(20, 20))
            
            master_icon_path = get_resource_path(os.path.join("src", "assets", "icons", "master_password.png"))
            if os.path.exists(master_icon_path):
                master_button.setIcon(QIcon(master_icon_path))
                master_button.setIconSize(QSize(20, 20))
            else:
                print(f"Ошибка: файл иконки мастер-пароля не найден: {master_icon_path}")
            
            button_layout.addWidget(create_button)
            button_layout.addWidget(master_button)
            frame_layout.addLayout(button_layout)
            
            self.strength_label.setStyleSheet(f"""
                color: {TEXT_COLOR};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_SMALL}px;
            """)
            self.strength_label.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(self.strength_label)
            
            self.combination_calculator = CombinationCalculator()
            frame_layout.addWidget(self.combination_calculator)
            
            self.update_strength_indicator()
            
        except Exception as e:
            print(f"Ошибка инициализации UI: {str(e)}")
            raise
        
    def _handle_toggle_click(self, event, toggle, original_handler):
        original_handler(event)
        self.update_strength_indicator()
        
    def _update_typewriter(self):
        if self.current_index <= len(self.current_password):
            displayed_text = self.current_password[:self.current_index]
            if self.current_index < len(self.current_password):
                displayed_text += "▌"
            self.password_field.setText(displayed_text)
            self.current_index += 1
        else:
            self.typewriter_timer.stop()
            self.password_field.setText(self.current_password)

    def generate_password(self):
        try:
            password = self.password_generator.generate(
                length=self.length_slider.value(),
                use_upper=self.toggles['upper']._enabled,
                use_lower=self.toggles['lower']._enabled,
                use_digits=self.toggles['digits']._enabled,
                use_special=self.toggles['special']._enabled
            )
            
            self.current_password = password
            self.current_index = 0
            self.password_field.setText("▌")
            
            self.typewriter_timer.start(50)
            
            strength = self.password_generator.check_strength(password)
            
            self.strength_label.setText(f"Фактическая сложность: {strength}%")
            
            if strength >= 75:
                color = SUCCESS_COLOR
            elif strength >= 50:
                color = WARNING_COLOR
            else:
                color = ERROR_COLOR
                
            self.strength_label.setStyleSheet(f"""
                color: {color};
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_SMALL}px;
                font-weight: bold;
            """)
            
            QTimer.singleShot(5000, self.update_strength_indicator)
            
        except ValueError:
            self.password_field.setStyleSheet(f"""
                QLabel {{
                    background-color: {ERROR_COLOR};
                    color: {TEXT_COLOR};
                    padding: 5px;
                    border-radius: 5px;
                    font-family: {FONT_FAMILY};
                    font-size: {FONT_SIZE_NORMAL}px;
                }}
            """)
            self.password_field.setText("Выберите тип символов")
            QTimer.singleShot(1000, self.reset_password_field_style)
            
    def copy_to_clipboard(self):
        if self.password_field.text() != "Нажмите кнопку" and not self.typewriter_timer.isActive():
            QApplication.clipboard().setText(self.current_password)
            original_text = self.password_field.text()
            self.password_field.setText("Пароль скопирован в буфер обмена")
            QTimer.singleShot(2000, lambda: self.password_field.setText(original_text))
            
    def reset_password_field_style(self):
        self.password_field.setStyleSheet(f"""
            QLabel {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                padding: 5px;
                border-radius: 5px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
            }}
        """)
        
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
        if event.button() == Qt.LeftButton:
            self.dragPos = None
            QApplication.restoreOverrideCursor()
            event.accept()

    def show_master_dialog(self):
        dialog = MasterPasswordDialog(self)
        dialog.exec_() 