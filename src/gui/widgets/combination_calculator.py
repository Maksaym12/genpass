from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QWidget, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from src.utils.styles import *
from src.gui.widgets.custom_widgets import CloseButton
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = "."
    return os.path.join(base_path, relative_path)

class FormulaExplanationDialog(QDialog):
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
        self.setFixedSize(450, 450)
        
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
        title_bar_layout.addWidget(icon_label)
        
        title = QLabel("Формула расчета комбинаций")
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
        
        formula_container = QFrame()
        formula_layout = QVBoxLayout(formula_container)
        formula_layout.setContentsMargins(0, 0, 0, 0)
        formula_layout.setSpacing(5)
        
        formula = QLabel(
            "Формула расчета:\n"
            "C = N^L\n\n"
            "Пример расчета:\n"
            "N = 26 + 26 + 10 + 33 = 95 символов\n"
            "L = 8 символов\n"
            "C = 95^8 ≈ 6.6 × 10^15 комбинаций"
        )
        formula.setStyleSheet(f"""
            color: {WARNING_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            font-weight: bold;
        """)
        formula.setWordWrap(True)
        
        explanation = QLabel(
            "Где в формуле:\n\n"
            "• N - общее количество символов в алфавите\n"
            "• L - длина пароля в символах\n"
            "• C - количество возможных комбинаций\n\n"
            "Алфавит (N) состоит из:\n"
            "• Прописные буквы (A-Z):   26 символов\n"
            "• Строчные буквы (a-z):    26 символов\n"
            "• Цифры (0-9):             10 символов\n"
            "• Специальные символы:      33 символа\n\n"
            "В примере выше показан расчет для случая,\n"
            "когда выбраны все типы символов (N = 95)\n"
            "и длина пароля 8 символов (L = 8).\n\n"
            "Чем больше разных типов символов и длина пароля,\n"
            "тем сложнее его взломать."
        )
        explanation.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
        """)
        explanation.setWordWrap(True)
        
        formula_layout.addWidget(formula)
        formula_layout.addWidget(explanation)
        frame_layout.addWidget(formula_container)

class CombinationCalculator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_SECONDARY};
                border-radius: 7px;
            }}
        """)
        
        formula_container = QHBoxLayout()
        
        self.formula_label = QLabel()
        self.formula_label.setStyleSheet(f"""
            color: {WARNING_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
            font-weight: bold;
        """)
        self.formula_label.setAlignment(Qt.AlignCenter)
        formula_container.addWidget(self.formula_label)
        
        help_button = QPushButton("?") 
        help_button.setFixedSize(16, 16)
        help_button.setCursor(Qt.PointingHandCursor)
        help_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {WARNING_COLOR};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 8px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_SMALL}px;
                font-weight: bold;
                padding-bottom: 2px;
            }}
            QPushButton:hover {{
                background-color: {WARNING_HOVER};
            }}
        """)
        help_button.clicked.connect(self.show_formula_explanation)
        formula_container.addWidget(help_button)
        
        self.result_label = QLabel()
        self.result_label.setStyleSheet(f"""
            color: {TEXT_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_SMALL}px;
        """)
        self.result_label.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(formula_container)
        layout.addWidget(self.result_label)
        
    def show_formula_explanation(self):
        dialog = FormulaExplanationDialog(self)
        parent_center = self.window().geometry().center()
        dialog.move(parent_center.x() - dialog.width() // 2,
                   parent_center.y() - dialog.height() // 2)
        dialog.exec_()
        
    def update_combinations(self, length, use_upper, use_lower, use_digits, use_special):
        alphabet_size = 0
        components = []
        
        if use_upper:
            alphabet_size += 26
            components.append("26 (A-Z)")
        if use_lower:
            alphabet_size += 26
            components.append("26 (a-z)")
        if use_digits:
            alphabet_size += 10
            components.append("10 (0-9)")
        if use_special:
            alphabet_size += 33
            components.append("33 (!@#)")
            
        if components:
            formula = " + ".join(components)
            total_combinations = alphabet_size ** length
            
            if total_combinations < 1000:
                formatted_result = str(total_combinations)
            elif total_combinations < 1_000_000:
                formatted_result = f"{total_combinations:,}".replace(",", " ")
            else:
                power = len(str(total_combinations)) - 1
                base = total_combinations / (10 ** power)
                formatted_result = f"{base:.2f} × 10^{power}"
            
            self.formula_label.setText(f"C = ({formula})^{length}")
            self.result_label.setText(f"Всего комбинаций: {formatted_result}")
        else:
            self.formula_label.setText("C = 0")
            self.result_label.setText("Выберите хотя бы один тип символов") 