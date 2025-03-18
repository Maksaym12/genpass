from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QFrame, QComboBox, QWidget, QSlider,
                           QCheckBox, QSpinBox, QPushButton, QTabWidget,
                           QScrollArea, QApplication, QColorDialog, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, QSettings, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QColor
import os
import sys
from src.utils.styles import *
from src.gui.widgets.custom_widgets import CloseButton, CustomSlider
from src.core.password_generator import PasswordGenerator

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SettingsDialog(QDialog):
    tray_setting_changed = pyqtSignal(bool)
    algorithm_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = None
        self.title_bar = None
        self.settings = QSettings("GenPass", "PasswordGenerator")
        
        self.auto_copy = self.settings.value("auto_copy", False, type=bool)
        self.clear_clipboard = self.settings.value("clear_clipboard", True, type=bool)
        self.clipboard_timeout = self.settings.value("clipboard_timeout", 30, type=int)
        self.default_length = self.settings.value("default_length", 12, type=int)
        self.exclude_similar = self.settings.value("exclude_similar", False, type=bool)
        self.show_exit_dialog = not self.settings.value("exit_dont_ask_again", False, type=bool)
        self.minimize_to_tray = self.settings.value("minimize_to_tray", False, type=bool)
        self.password_algorithm = self.settings.value("password_algorithm", PasswordGenerator.ALGORITHM_SECRETS, type=str)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(450, 500)
        
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
        icon_path = get_resource_path(os.path.join("src", "assets", "icons", "settings_icon.png"))
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        else:
            print(f"Ошибка: файл иконки не найден: {icon_path}")
        title_bar_layout.addWidget(icon_label)
        
        title = QLabel("Настройки приложения")
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
        close_button.clicked.connect(self.close)
        
        title_bar_layout.addWidget(close_button)
        frame_layout.addWidget(title_bar)
        
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget {{
                background-color: {DARK_PRIMARY};
                border: none;
            }}
            QTabWidget::pane {{
                border: none;
                background-color: {DARK_SECONDARY};
                border-radius: 5px;
            }}
            QTabBar::tab {{
                background-color: {BUTTON_COLOR};
                color: {TEXT_COLOR};
                border: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }}
            QTabBar::tab:selected {{
                background-color: {ACCENT_COLOR};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {BUTTON_HOVER};
            }}
        """)
        
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setContentsMargins(10, 10, 10, 10)
        general_layout.setSpacing(15)
        
        algorithm_layout = QHBoxLayout()
        algorithm_label = QLabel("Алгоритм генерации паролей:")
        algorithm_label.setStyleSheet(f"color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        
        algorithm_combo = QComboBox()
        algorithm_combo.addItem("Стандартный (cryptosecure)", PasswordGenerator.ALGORITHM_SECRETS)
        algorithm_combo.addItem("Фонетический (произносимый)", PasswordGenerator.ALGORITHM_PHONETIC)
        algorithm_combo.addItem("Шаблонный (равномерный)", PasswordGenerator.ALGORITHM_PATTERN)
        algorithm_combo.addItem("Запоминающийся (слова+цифры)", PasswordGenerator.ALGORITHM_MEMORABLE)
        
        index = algorithm_combo.findData(self.password_algorithm)
        if index >= 0:
            algorithm_combo.setCurrentIndex(index)
        
        algorithm_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                border: 1px solid {BUTTON_HOVER};
                border-radius: 4px;
                padding: 4px;
                min-width: 180px;
            }}
            QComboBox:drop-down {{
                width: 20px;
                border-left: 1px solid {BUTTON_HOVER};
            }}
            QComboBox QAbstractItemView {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                selection-background-color: {ACCENT_COLOR};
                selection-color: {TEXT_COLOR};
            }}
        """)
        algorithm_combo.currentIndexChanged.connect(self.save_password_algorithm)
        
        algorithm_layout.addWidget(algorithm_label)
        algorithm_layout.addStretch()
        algorithm_layout.addWidget(algorithm_combo)
        general_layout.addLayout(algorithm_layout)
        
        self.algorithm_info_label = QLabel()
        self.algorithm_info_label.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
            font-style: italic;
        """)
        self.algorithm_info_label.setWordWrap(True)
        self.update_algorithm_info(algorithm_combo.currentIndex())
        general_layout.addWidget(self.algorithm_info_label)
        
        algorithm_combo.currentIndexChanged.connect(self.update_algorithm_info)
        
        length_layout = QHBoxLayout()
        length_label = QLabel("Длина пароля по умолчанию:")
        length_label.setStyleSheet(f"color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        
        length_spinner = QSpinBox()
        length_spinner.setRange(6, 32)
        length_spinner.setValue(self.default_length)
        length_spinner.setStyleSheet(f"""
            QSpinBox {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                border: 1px solid {BUTTON_HOVER};
                border-radius: 4px;
                padding: 4px;
                min-width: 60px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {BUTTON_COLOR};
                border-radius: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {BUTTON_HOVER};
            }}
        """)
        length_spinner.valueChanged.connect(self.save_default_length)
        
        length_layout.addWidget(length_label)
        length_layout.addStretch()
        length_layout.addWidget(length_spinner)
        general_layout.addLayout(length_layout)
        
        exclude_similar_check = QCheckBox("Исключать похожие символы (1, l, I, 0, O)")
        exclude_similar_check.setChecked(self.exclude_similar)
        exclude_similar_check.setStyleSheet(f"""
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
        exclude_similar_check.stateChanged.connect(self.save_exclude_similar)
        general_layout.addWidget(exclude_similar_check)
        
        auto_copy_check = QCheckBox("Автоматически копировать пароль в буфер обмена")
        auto_copy_check.setChecked(self.auto_copy)
        auto_copy_check.setStyleSheet(f"""
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
        auto_copy_check.stateChanged.connect(self.save_auto_copy)
        general_layout.addWidget(auto_copy_check)
        
        clear_clipboard_check = QCheckBox("Очищать буфер обмена через указанное время")
        clear_clipboard_check.setChecked(self.clear_clipboard)
        clear_clipboard_check.setStyleSheet(f"""
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
        clear_clipboard_check.stateChanged.connect(self.save_clear_clipboard)
        general_layout.addWidget(clear_clipboard_check)
        
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Время до очистки буфера обмена (секунд):")
        timeout_label.setStyleSheet(f"color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        
        timeout_spinner = QSpinBox()
        timeout_spinner.setRange(5, 300)
        timeout_spinner.setValue(self.clipboard_timeout)
        timeout_spinner.setStyleSheet(f"""
            QSpinBox {{
                background-color: {DARK_SECONDARY};
                color: {TEXT_COLOR};
                border: 1px solid {BUTTON_HOVER};
                border-radius: 4px;
                padding: 4px;
                min-width: 60px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {BUTTON_COLOR};
                border-radius: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {BUTTON_HOVER};
            }}
        """)
        timeout_spinner.valueChanged.connect(self.save_clipboard_timeout)
        
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addStretch()
        timeout_layout.addWidget(timeout_spinner)
        general_layout.addLayout(timeout_layout)
        
        general_layout.addStretch()
        
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout(advanced_tab)
        advanced_layout.setContentsMargins(10, 10, 10, 10)
        advanced_layout.setSpacing(15)
        
        exit_label = QLabel("Закрытие приложения")
        exit_label.setStyleSheet(f"""
            color: {ACCENT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            font-weight: bold;
        """)
        advanced_layout.addWidget(exit_label)
        
        exit_dialog_check = QCheckBox("Показывать диалог подтверждения при выходе")
        exit_dialog_check.setChecked(self.show_exit_dialog)
        exit_dialog_check.setStyleSheet(f"""
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
        exit_dialog_check.stateChanged.connect(self.save_exit_dialog)
        advanced_layout.addWidget(exit_dialog_check)
        
        minimize_to_tray_check = QCheckBox("Сворачивать в системный трей при нажатии на кнопку Свернуть")
        minimize_to_tray_check.setChecked(self.minimize_to_tray)
        minimize_to_tray_check.setStyleSheet(f"""
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
        minimize_to_tray_check.stateChanged.connect(self.save_minimize_to_tray)
        advanced_layout.addWidget(minimize_to_tray_check)
        
        advanced_layout.addStretch()
        
        info_label = QLabel("Настройки на этой вкладке влияют на поведение приложения и требуют перезапуска для применения всех изменений.")
        info_label.setStyleSheet(f"color: {TEXT_COLOR}; font-family: {FONT_FAMILY};")
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        advanced_layout.addWidget(info_label)
        
        tab_widget.addTab(general_tab, "Основные")
        tab_widget.addTab(advanced_tab, "Дополнительно")
        
        frame_layout.addWidget(tab_widget)
        
        button_layout = QHBoxLayout()
        
        default_button = QPushButton("По умолчанию")
        default_button.setCursor(Qt.PointingHandCursor)
        default_button.setStyleSheet(f"""
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
        default_button.clicked.connect(self.reset_to_default)
        
        ok_button = QPushButton("ОК")
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_COLOR};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: {ACCENT_HOVER};
            }}
        """)
        ok_button.clicked.connect(self.accept)
        
        button_layout.addWidget(default_button)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        
        frame_layout.addLayout(button_layout)
        
    def update_algorithm_info(self, index):
        combo = self.sender() if self.sender() else None
        if combo and isinstance(combo, QComboBox):
            algorithm = combo.itemData(index)
        else:
            algorithm = self.password_algorithm
            
        if algorithm == PasswordGenerator.ALGORITHM_SECRETS:
            self.algorithm_info_label.setText("Стандартный алгоритм - использует криптографически стойкий генератор случайных чисел для создания максимально непредсказуемых паролей.")
        elif algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
            self.algorithm_info_label.setText("Фонетический алгоритм - создаёт пароли, которые легче запомнить и произнести благодаря чередованию гласных и согласных.")
        elif algorithm == PasswordGenerator.ALGORITHM_PATTERN:
            self.algorithm_info_label.setText("Шаблонный алгоритм - равномерно распределяет разные типы символов в пароле, обеспечивая хороший баланс между типами символов.")
        elif algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
            self.algorithm_info_label.setText("Алгоритм запоминаемых паролей - создаёт пароли на основе слов со специальными символами и цифрами. Легко запомнить, но длиннее обычных паролей.")
            
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
    
    def save_auto_copy(self, state):
        self.auto_copy = (state == Qt.Checked)
        self.settings.setValue("auto_copy", self.auto_copy)
    
    def save_clear_clipboard(self, state):
        self.clear_clipboard = (state == Qt.Checked)
        self.settings.setValue("clear_clipboard", self.clear_clipboard)
    
    def save_clipboard_timeout(self, value):
        self.clipboard_timeout = value
        self.settings.setValue("clipboard_timeout", value)
    
    def save_default_length(self, value):
        self.default_length = value
        self.settings.setValue("default_length", value)
    
    def save_exclude_similar(self, state):
        self.exclude_similar = (state == Qt.Checked)
        self.settings.setValue("exclude_similar", self.exclude_similar)
    
    def save_exit_dialog(self, state):
        self.show_exit_dialog = (state == Qt.Checked)
        self.settings.setValue("exit_dont_ask_again", not (state == Qt.Checked))
    
    def save_minimize_to_tray(self, state):
        old_value = self.minimize_to_tray
        self.minimize_to_tray = (state == Qt.Checked)
        self.settings.setValue("minimize_to_tray", self.minimize_to_tray)
        
        if old_value != self.minimize_to_tray:
            self.tray_setting_changed.emit(self.minimize_to_tray)
    
    def save_password_algorithm(self, index):
        combo = self.sender()
        algorithm = combo.itemData(index)
        
        old_algorithm = self.password_algorithm
        self.password_algorithm = algorithm
        self.settings.setValue("password_algorithm", algorithm)
        
        if old_algorithm != algorithm:
            self.algorithm_changed.emit(algorithm)
    
    def reset_to_default(self):
        old_minimize_to_tray = self.minimize_to_tray
        old_algorithm = self.password_algorithm
        
        self.settings.setValue("auto_copy", False)
        self.settings.setValue("clear_clipboard", True)
        self.settings.setValue("clipboard_timeout", 30)
        self.settings.setValue("default_length", 12)
        self.settings.setValue("exclude_similar", False)
        self.settings.setValue("exit_dont_ask_again", False)
        self.settings.setValue("minimize_to_tray", False)
        self.settings.setValue("password_algorithm", PasswordGenerator.ALGORITHM_SECRETS)
        
        self.auto_copy = False
        self.clear_clipboard = True
        self.clipboard_timeout = 30
        self.default_length = 12
        self.exclude_similar = False
        self.show_exit_dialog = True
        self.minimize_to_tray = False
        self.password_algorithm = PasswordGenerator.ALGORITHM_SECRETS
        
        if old_minimize_to_tray != self.minimize_to_tray:
            self.tray_setting_changed.emit(self.minimize_to_tray)
            
        if old_algorithm != self.password_algorithm:
            self.algorithm_changed.emit(self.password_algorithm)
        
        QMessageBox.information(self, "Сброс настроек", "Настройки сброшены до значений по умолчанию. Перезапустите приложение для применения всех изменений.")
        self.accept() 