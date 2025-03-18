from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame, QApplication, QPushButton, QCheckBox, QDialog,
                             QSystemTrayIcon, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QSize, QSettings, QEvent
from PyQt5.QtGui import QFont, QIcon, QPixmap
import os
import sys
from src.utils.styles import *
from src.gui.widgets.custom_widgets import AnimatedToggle, CustomSlider, AnimatedButton, CloseButton, MinimizeButton
from src.gui.widgets.help_dialog import HelpButton, HelpDialog
from src.gui.widgets.about_dialog import AboutDialog
from src.gui.widgets.combination_calculator import CombinationCalculator
from src.gui.widgets.master_password_dialog import MasterPasswordDialog
from src.gui.widgets.sidebar_buttons import SettingsButton, AboutButton, UUIDButton
from src.gui.widgets.exit_dialog import ExitDialog
from src.gui.widgets.system_tray import SystemTray
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
        
        self.settings = QSettings("GenPass", "PasswordGenerator")
        self.default_length = self.settings.value("default_length", 12, type=int)
        self.exclude_similar = self.settings.value("exclude_similar", False, type=bool)
        self.auto_copy = self.settings.value("auto_copy", False, type=bool)
        self.clear_clipboard = self.settings.value("clear_clipboard", True, type=bool)
        self.clipboard_timeout = self.settings.value("clipboard_timeout", 30, type=int)
        self.minimize_to_tray = self.settings.value("minimize_to_tray", False, type=bool)
        
        self.password_algorithm = self.settings.value("password_algorithm", PasswordGenerator.ALGORITHM_SECRETS, type=str)
        
        try:
            self.password_generator.set_algorithm(self.password_algorithm)
        except ValueError:
            self.password_algorithm = PasswordGenerator.ALGORITHM_SECRETS
            self.password_generator.set_algorithm(self.password_algorithm)
        
        self.tray_icon = None
        if QSystemTrayIcon.isSystemTrayAvailable() and self.minimize_to_tray:
            self.tray_icon = SystemTray(self)
            self.tray_icon.show()
        
        self.initUI()
        
        self.apply_algorithm_ui_restrictions()
        
        self.update_toggle_visual_state()
        
    def update_strength_indicator(self):
        length = self.length_slider.value()
        use_upper = self.toggles['upper']._enabled
        use_lower = self.toggles['lower']._enabled
        use_digits = self.toggles['digits']._enabled
        use_special = self.toggles['special']._enabled
        
        if self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
            use_upper = True
            use_lower = True
        elif self.password_algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
            use_lower = True
        
        self.combination_calculator.update_combinations(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_special=use_special,
            algorithm=self.password_algorithm
        )
        
        active_types = [use_upper, use_lower, use_digits, use_special]
        if not any(active_types):
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
            
            if self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                estimated_length = 12
                if use_digits:
                    estimated_length += 2  # Обычно 2 цифры
                if use_special:
                    estimated_length += 1  # Обычно 1 спецсимвол
                
                test_password = "TestPassword"
                if use_digits:
                    test_password += "12"
                if use_special:
                    test_password += "!"
            
            strength = self.password_generator.check_strength(test_password)
            
            algorithm_info = ""
            if self.password_algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
                algorithm_info = " (Произносимый)"
            elif self.password_algorithm == PasswordGenerator.ALGORITHM_PATTERN:
                algorithm_info = " (Шаблонный)"
            elif self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                algorithm_info = " (Запоминаемый)"
                
            self.strength_label.setText(f"Примерная сложность{algorithm_info}: {strength}%")
        
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
            main_layout = QHBoxLayout(main_widget)
            main_layout.setContentsMargins(7, 7, 7, 7)
            main_layout.setSpacing(7)
            
            content_widget = QWidget()
            layout = QVBoxLayout(content_widget)
            layout.setContentsMargins(0, 0, 0, 0)
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
            
            main_layout.addWidget(content_widget)
            
            sidebar_widget = QWidget()
            sidebar_widget.setFixedWidth(SIDEBAR_WIDTH)
            sidebar_layout = QVBoxLayout(sidebar_widget)
            sidebar_layout.setContentsMargins(0, 0, 0, 0)
            sidebar_layout.setSpacing(10)
            
            sidebar_frame = QFrame()
            sidebar_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {SIDEBAR_COLOR};
                    border-radius: 13px;
                }}
            """)
            sidebar_inner_layout = QVBoxLayout(sidebar_frame)
            sidebar_inner_layout.setContentsMargins(5, 10, 5, 10)
            sidebar_inner_layout.setSpacing(15)
            sidebar_inner_layout.setAlignment(Qt.AlignTop)
            
            settings_button = SettingsButton()
            sidebar_inner_layout.addWidget(settings_button, 0, Qt.AlignCenter)
            
            uuid_button = UUIDButton()
            sidebar_inner_layout.addWidget(uuid_button, 0, Qt.AlignCenter)
            
            sidebar_inner_layout.addStretch()
            
            about_button = AboutButton()
            sidebar_inner_layout.addWidget(about_button, 0, Qt.AlignCenter)
            
            sidebar_layout.addWidget(sidebar_frame)
            
            main_layout.addWidget(sidebar_widget)
            
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
            minimize_button = MinimizeButton()
            minimize_button.clicked.connect(self.handle_minimize)
            close_button = CloseButton()
            close_button.clicked.connect(self.close)
            
            title_bar_layout.addWidget(help_button)
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
            
            length_label = QLabel(f"Длина пароля: {self.default_length} символов (по умолчанию)")
            length_label.setStyleSheet(f"color: {TEXT_COLOR}; font-size: {FONT_SIZE_NORMAL}px;")
            frame_layout.addWidget(length_label)
            
            self.length_label = length_label
            
            self.length_slider = CustomSlider()
            self.length_slider.setRange(6, 32)
            self.length_slider.setValue(self.default_length)
            self.length_slider.valueChanged.connect(
                lambda v: (self.length_label.setText(f"Длина пароля: {v} символов"), self.update_strength_indicator())
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
            if self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                password = self.password_generator.generate(
                    length=0,  
                    use_upper=True,     
                    use_lower=True,
                    use_digits=self.toggles['digits']._enabled,
                    use_special=self.toggles['special']._enabled
                )
            elif self.password_algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
                password = self.password_generator.generate(
                    length=self.length_slider.value(),
                    use_upper=self.toggles['upper']._enabled,
                    use_lower=True,
                    use_digits=self.toggles['digits']._enabled,
                    use_special=self.toggles['special']._enabled
                )
            else:
                password = self.password_generator.generate(
                    length=self.length_slider.value(),
                    use_upper=self.toggles['upper']._enabled,
                    use_lower=self.toggles['lower']._enabled,
                    use_digits=self.toggles['digits']._enabled,
                    use_special=self.toggles['special']._enabled
                )
            
            has_active_types = False
            
            if self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                has_active_types = True
            elif self.password_algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
                has_active_types = self.toggles['upper']._enabled or self.toggles['digits']._enabled or self.toggles['special']._enabled
            else:
                has_active_types = any([
                    self.toggles['upper']._enabled, 
                    self.toggles['lower']._enabled,
                    self.toggles['digits']._enabled,
                    self.toggles['special']._enabled
                ])
            
            if not has_active_types:
                raise ValueError("Выберите хотя бы один тип символов")
            
            self.current_password = password
            self.current_index = 0
            self.password_field.setText("▌")
            
            self.typewriter_timer.start(50)
            
            if self.auto_copy:
                QTimer.singleShot(len(password) * 50 + 200, self.auto_copy_to_clipboard)
            
            strength = self.password_generator.check_strength(password)
            
            algorithm_info = ""
            if self.password_algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
                algorithm_info = " (Произносимый)"
            elif self.password_algorithm == PasswordGenerator.ALGORITHM_PATTERN:
                algorithm_info = " (Шаблонный)"
            elif self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                algorithm_info = " (Запоминаемый)"
                
            self.strength_label.setText(f"Фактическая сложность{algorithm_info}: {strength}%")
            
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
            
            actual_length = len(password)
            if self.password_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                self.combination_calculator.update_combinations(
                    length=actual_length,
                    use_upper=True,
                    use_lower=True,
                    use_digits=self.toggles['digits']._enabled,
                    use_special=self.toggles['special']._enabled,
                    algorithm=self.password_algorithm
                )
            
            QTimer.singleShot(5000, self.update_strength_indicator)
            
        except ValueError as e:
            error_message = str(e) if str(e) else "Выберите хотя бы один тип символов"
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
            self.password_field.setText(error_message)
            QTimer.singleShot(1500, self.reset_password_field_style)
            
    def auto_copy_to_clipboard(self):
        if self.current_password and not self.typewriter_timer.isActive():
            QApplication.clipboard().setText(self.current_password)
            
            if self.clear_clipboard:
                QTimer.singleShot(self.clipboard_timeout * 1000, self.clear_clipboard_contents)
        else:
            QTimer.singleShot(100, self.auto_copy_to_clipboard)
            
    def copy_to_clipboard(self, auto_copied=False):
        if self.current_password and self.password_field.text() != "Нажмите кнопку для генерации пароля" and not self.typewriter_timer.isActive():
            QApplication.clipboard().setText(self.current_password)
            original_text = self.password_field.text()
            self.password_field.setText("Пароль скопирован в буфер обмена")
            QTimer.singleShot(2000, lambda: self.password_field.setText(original_text))
            
            if self.clear_clipboard:
                QTimer.singleShot(self.clipboard_timeout * 1000, self.clear_clipboard_contents)
    
    def clear_clipboard_contents(self):
        clipboard = QApplication.clipboard()
        if clipboard.text() == self.current_password:
            clipboard.clear()
            
        
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

    def closeEvent(self, event):
        dont_ask_again = self.settings.value("exit_dont_ask_again", False, type=bool)
        
        if dont_ask_again:
            event.accept()
            return
            
        dialog = ExitDialog(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            event.accept()
        else:
            event.ignore()
    
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized() and self.minimize_to_tray and self.tray_icon:
            # Скрываем окно
            self.hide()
            # Показываем уведомление в трее
            self.tray_icon.show_message("GenPass", "Приложение свернуто в трей", QSystemTrayIcon.Information, 2000)
            event.ignore()
        else:
            super().changeEvent(event)

    def handle_minimize(self):
        if self.minimize_to_tray and self.tray_icon:
            self.hide()
            self.tray_icon.show_message("GenPass", "Приложение свернуто в трей", QSystemTrayIcon.Information, 2000)
        else:
            self.showMinimized()
            
    def update_tray_icon(self, show_tray):
        self.minimize_to_tray = show_tray
        
        if show_tray:
            if self.tray_icon is None and QSystemTrayIcon.isSystemTrayAvailable():
                self.tray_icon = SystemTray(self)
                self.tray_icon.show()
        else:
            if self.tray_icon is not None:
                self.tray_icon.hide()
                self.tray_icon.deleteLater()
                self.tray_icon = None 
                
    def apply_algorithm_ui_restrictions(self):
        self.update_algorithm(self.password_algorithm)
        
    def update_toggle_visual_state(self):
        algorithm = self.password_generator.current_algorithm
        
        for toggle_key, toggle in self.toggles.items():
            feature_active = True
            reason = ""
            
            if algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                if toggle_key == 'upper' or toggle_key == 'lower' or toggle_key == 'digits':
                    feature_active = False
                    reason = "Всегда включено для алгоритма Запоминаемых паролей"
            elif algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
                if toggle_key == 'lower':
                    feature_active = False
                    reason = "Недоступно для Фонетического алгоритма"
            elif algorithm == PasswordGenerator.ALGORITHM_PATTERN:
                feature_active = False
                reason = "Недоступно для Шаблонного алгоритма"
            
            toggle_layouts = []
            for i in range(self.centralWidget().layout().count()):
                widget = self.centralWidget().layout().itemAt(i).widget()
                if isinstance(widget, QWidget):
                    for j in range(widget.layout().count()):
                        item = widget.layout().itemAt(j)
                        if item.widget() and isinstance(item.widget(), QFrame):
                            frame = item.widget()
                            for k in range(frame.layout().count()):
                                item_in_frame = frame.layout().itemAt(k)
                                if item_in_frame.layout() and isinstance(item_in_frame.layout(), QHBoxLayout):
                                    for m in range(item_in_frame.layout().count()):
                                        if item_in_frame.layout().itemAt(m).widget() == toggle:
                                            toggle_layouts.append(item_in_frame.layout())
                                            break
            
            if not toggle_layouts:
                continue
                
            toggle_layout = toggle_layouts[0]
            
            lock_icon = None
            for i in range(toggle_layout.count()):
                widget = toggle_layout.itemAt(i).widget()
                if widget and widget.objectName() == "lock_icon_" + toggle_key:
                    lock_icon = widget
                    break
            
            if feature_active:
                toggle.setEnabled(True)
                toggle.setToolTip("")
                
                if lock_icon:
                    lock_icon.deleteLater()
            else:
                toggle.setEnabled(False)
                
                toggle.setToolTip("")
                
                tooltip = f"Функция отключена: {reason}"
                
                if not lock_icon:
                    lock_icon_path = "src/assets/icons/lock.png"
                    if not os.path.exists(lock_icon_path):
                        lock_icon_path = get_resource_path(os.path.join("src", "assets", "icons", "lock.png"))
                    
                    if os.path.exists(lock_icon_path):
                        text_label = None
                        for i in range(toggle_layout.count()):
                            item = toggle_layout.itemAt(i)
                            if item.widget() and isinstance(item.widget(), QLabel) and item.widget().text():
                                text_label = item.widget()
                                break
                        
                        if text_label:
                            lock_icon = QLabel()
                            lock_icon.setObjectName("lock_icon_" + toggle_key)
                            lock_icon_pixmap = QPixmap(lock_icon_path)
                            lock_icon_pixmap = lock_icon_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            lock_icon.setPixmap(lock_icon_pixmap)
                            lock_icon.setFixedSize(16, 16)
                            lock_icon.setAlignment(Qt.AlignCenter)
                            lock_icon.setToolTip(tooltip)
                            
                            container = QWidget()
                            container.setFixedWidth(24)
                            container_layout = QHBoxLayout(container)
                            container_layout.setContentsMargins(0, 0, 0, 0)
                            container_layout.addWidget(lock_icon)
                            
                            toggle_layout.insertWidget(1, container)
                else:
                    for i in range(toggle_layout.count()):
                        widget = toggle_layout.itemAt(i).widget()
                        if widget and hasattr(widget, 'children'):
                            for child in widget.children():
                                if isinstance(child, QLabel) and child.objectName() == "lock_icon_" + toggle_key:
                                    child.setToolTip(tooltip)
                                    break

    def update_algorithm(self, algorithm):
        try:
            if self.password_algorithm == algorithm:
                return
                
            self.password_algorithm = algorithm
            self.password_generator.set_algorithm(algorithm)
            
            self.clear_lock_icons()
            
            if algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
                self.length_slider.setEnabled(False)
                self.length_slider.setEnabled(False)
                self.length_label.setText(f"Длина пароля: авто (запоминаемый пароль)")
                
                self.toggles['upper'].setEnabled(False)
                self.toggles['lower'].setEnabled(False)
                self.toggles['digits'].setEnabled(False)
                
                if not self.toggles['upper']._enabled:
                    self.toggles['upper'].mousePressEvent(None)
                    
                if not self.toggles['lower']._enabled:
                    self.toggles['lower'].mousePressEvent(None)
                
                if not self.toggles['digits']._enabled:
                    self.toggles['digits'].mousePressEvent(None)
                
                self.toggles['special'].setEnabled(True)
                
                self.update_toggle_visual_state()
                
            elif algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
                self.length_slider.setEnabled(True)
                self.length_slider.setEnabled(True)
                self.length_label.setText(f"Длина пароля: {self.length_slider.value()} символов")
                
                self.toggles['lower'].setEnabled(False)
                if not self.toggles['lower']._enabled:
                    self.toggles['lower'].mousePressEvent(None)
                    
                self.toggles['upper'].setEnabled(True)
                
                self.toggles['digits'].setEnabled(True)
                self.toggles['special'].setEnabled(True)
                
                self.update_toggle_visual_state()
                
            elif algorithm == PasswordGenerator.ALGORITHM_PATTERN:
                self.length_slider.setEnabled(True)
                self.length_label.setText(f"Длина пароля: {self.length_slider.value()} символов")
                
                if not self.toggles['upper']._enabled:
                    self.toggles['upper'].mousePressEvent(None)
                if not self.toggles['lower']._enabled:
                    self.toggles['lower'].mousePressEvent(None)
                if not self.toggles['digits']._enabled:
                    self.toggles['digits'].mousePressEvent(None)
                if not self.toggles['special']._enabled:
                    self.toggles['special'].mousePressEvent(None)
                
                self.toggles['upper'].setEnabled(False)
                self.toggles['lower'].setEnabled(False)
                self.toggles['digits'].setEnabled(False)
                self.toggles['special'].setEnabled(False)
                
                self.update_toggle_visual_state()
                
            else:
                self.length_slider.setEnabled(True)
                self.length_label.setText(f"Длина пароля: {self.length_slider.value()} символов")
                
                self.toggles['upper'].setEnabled(True)
                self.toggles['lower'].setEnabled(True)
                self.toggles['digits'].setEnabled(True)
                self.toggles['special'].setEnabled(True)
                
                self.update_toggle_visual_state()
                
            self.update_strength_indicator()
            
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка алгоритма", str(e))
            self.password_algorithm = PasswordGenerator.ALGORITHM_SECRETS
            self.password_generator.set_algorithm(PasswordGenerator.ALGORITHM_SECRETS)
            
    def open_settings(self):
        from src.gui.widgets.settings_dialog import SettingsDialog
        
        dialog = SettingsDialog(self)
        dialog.tray_setting_changed.connect(self.update_tray_icon)
        dialog.algorithm_changed.connect(self.update_algorithm)
        
        if dialog.exec_() == QDialog.Accepted:
            self.default_length = dialog.default_length
            self.exclude_similar = dialog.exclude_similar
            self.auto_copy = dialog.auto_copy
            self.clear_clipboard = dialog.clear_clipboard
            self.clipboard_timeout = dialog.clipboard_timeout
            
            self.length_slider.setValue(self.default_length)
            
            self.clear_lock_icons()
            
            self.update_toggle_visual_state()
            
            self.update_strength_indicator()

    def clear_lock_icons(self):
        for i in range(self.centralWidget().layout().count()):
            widget = self.centralWidget().layout().itemAt(i).widget()
            if isinstance(widget, QWidget):
                for j in range(widget.layout().count()):
                    item = widget.layout().itemAt(j)
                    if item.widget() and isinstance(item.widget(), QFrame):
                        frame = item.widget()
                        for k in range(frame.layout().count()):
                            item_in_frame = frame.layout().itemAt(k)
                            if item_in_frame.layout() and isinstance(item_in_frame.layout(), QHBoxLayout):
                                layout = item_in_frame.layout()
                                for m in range(layout.count()-1, -1, -1):
                                    widget = layout.itemAt(m).widget()
                                    if widget:
                                        for child in widget.children():
                                            if isinstance(child, QLabel) and hasattr(child, 'objectName'):
                                                obj_name = child.objectName()
                                                if isinstance(obj_name, str) and obj_name.startswith("lock_icon_"):
                                                    layout.removeWidget(widget)
                                                    widget.setParent(None)
                                                    widget.deleteLater()
                                                    break 