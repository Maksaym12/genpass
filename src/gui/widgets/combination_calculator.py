from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QWidget, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from src.utils.styles import *
from src.gui.widgets.custom_widgets import CloseButton
from src.core.password_generator import PasswordGenerator
import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = "."
    return os.path.join(base_path, relative_path)

class FormulaExplanationDialog(QDialog):
    def __init__(self, algorithm=PasswordGenerator.ALGORITHM_SECRETS, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragPos = None
        self.title_bar = None
        self.algorithm = algorithm
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
        
        formula_text = ""
        explanation_text = ""
        
        if self.algorithm == PasswordGenerator.ALGORITHM_SECRETS:
            formula_text = (
                "Формула расчета:\n"
                "C = N^L\n\n"
                "Пример расчета:\n"
                "N = 26 + 26 + 10 + 33 = 95 символов\n"
                "L = 8 символов\n"
                "C = 95^8 ≈ 6.6 × 10^15 комбинаций"
            )
            
            explanation_text = (
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
        elif self.algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
            formula_text = (
                "Формула для фонетического алгоритма:\n"
                "C = (21^(L/2)) × (5^(L/2)) × k\n\n"
                "Пример расчета:\n"
                "21 согласных, 5 гласных, L = 8 символов\n"
                "k = 1.5 (коэффициент для цифр и спецсимволов)\n"
                "C ≈ 21^4 × 5^4 × 1.5 ≈ 1.1 × 10^7 комбинаций"
            )
            
            explanation_text = (
                "Где в формуле:\n\n"
                "• 21 - количество согласных букв\n"
                "• 5 - количество гласных букв\n"
                "• L - длина пароля в символах\n"
                "• k - коэффициент, учитывающий добавление цифр\n"
                "  и специальных символов\n"
                "• C - количество возможных комбинаций\n\n"
                "Фонетический алгоритм чередует согласные и гласные,\n"
                "что делает пароль легче произносимым, но снижает\n"
                "количество возможных комбинаций по сравнению со\n"
                "стандартным алгоритмом.\n\n"
                "Добавление цифр и специальных символов увеличивает\n"
                "энтропию, но в меньшей степени, чем в стандартном алгоритме."
            )
        elif self.algorithm == PasswordGenerator.ALGORITHM_PATTERN:
            formula_text = (
                "Формула для шаблонного алгоритма:\n"
                "C = (26^Lu) × (26^Ll) × (10^D) × (33^S)\n\n"
                "Пример расчета (использованы все символы, L = 8):\n"
                "Lu, Ll, D, S = 2 каждый (равномерное распределение)\n"
                "C = 26^2 × 26^2 × 10^2 × 33^2 ≈ 7.5 × 10^8 комбинаций"
            )
            
            explanation_text = (
                "Где в формуле:\n\n"
                "• Lu - число прописных букв (A-Z) в пароле\n"
                "• Ll - число строчных букв (a-z) в пароле\n"
                "• D - число цифр (0-9) в пароле\n"
                "• S - число спецсимволов в пароле\n"
                "• C - количество возможных комбинаций\n\n"
                "Шаблонный алгоритм создает равномерное распределение\n"
                "различных типов символов. Это повышает случайность\n"
                "расположения символов в пароле, но общее число комбинаций\n"
                "может быть ниже, чем в стандартном алгоритме.\n\n"
                "Такой подход гарантирует использование всех типов символов,\n"
                "что важно для соответствия требованиям многих систем\n"
                "к паролям."
            )
        elif self.algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
            formula_text = (
                "Формула для запоминаемого алгоритма:\n"
                "C = W^2 × 10^Nd × 33^Ns\n\n"
                "Пример расчета:\n"
                "W = 32 (словарь), Nd = 2 (цифры), Ns = 1 (спецсимволы)\n"
                "C = 32^2 × 10^2 × 33^1 ≈ 3.5 × 10^6 комбинаций"
            )
            
            explanation_text = (
                "Где в формуле:\n\n"
                "• W - размер словаря (количество слов)\n"
                "• Nd - количество цифр в пароле\n"
                "• Ns - количество специальных символов\n"
                "• C - количество возможных комбинаций\n\n"
                "Запоминаемый алгоритм создает пароли на основе слов\n"
                "из словаря, дополненных цифрами и специальными символами.\n\n"
                "Такой пароль легче запомнить, но общее число комбинаций\n"
                "существенно ниже, чем в стандартном алгоритме.\n"
                "Для повышения безопасности используются два слова\n"
                "с измененным регистром первой буквы."
            )
        
        formula = QLabel(formula_text)
        formula.setStyleSheet(f"""
            color: {WARNING_COLOR};
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE_NORMAL}px;
            font-weight: bold;
        """)
        formula.setWordWrap(True)
        
        explanation = QLabel(explanation_text)
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
        self.current_algorithm = PasswordGenerator.ALGORITHM_SECRETS
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
        dialog = FormulaExplanationDialog(self.current_algorithm, self)
        parent_center = self.window().geometry().center()
        dialog.move(parent_center.x() - dialog.width() // 2,
                   parent_center.y() - dialog.height() // 2)
        dialog.exec_()
        
    def update_combinations(self, length, use_upper, use_lower, use_digits, use_special, algorithm=None):
        if algorithm is not None:
            self.current_algorithm = algorithm
            
        if self.current_algorithm == PasswordGenerator.ALGORITHM_SECRETS:
            self._update_standard_combinations(length, use_upper, use_lower, use_digits, use_special)
        elif self.current_algorithm == PasswordGenerator.ALGORITHM_PHONETIC:
            self._update_phonetic_combinations(length, use_digits, use_special)
        elif self.current_algorithm == PasswordGenerator.ALGORITHM_PATTERN:
            self._update_pattern_combinations(length, use_upper, use_lower, use_digits, use_special)
        elif self.current_algorithm == PasswordGenerator.ALGORITHM_MEMORABLE:
            self._update_memorable_combinations(use_digits, use_special)
            
    def _update_standard_combinations(self, length, use_upper, use_lower, use_digits, use_special):
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
    
    def _update_phonetic_combinations(self, length, use_digits, use_special):
        # Расчет для фонетического алгоритма
        consonants = 21 
        vowels = 5 
        
        # Расчет комбинаций для чередования гласных и согласных
        consonant_part = consonants ** (length // 2 + (length % 2))
        vowel_part = vowels ** (length // 2)
        
        total_combinations = consonant_part * vowel_part
        
        digit_spec_multiplier = 1.0
        if use_digits:
            digit_spec_multiplier *= 1.2
        if use_special:
            digit_spec_multiplier *= 1.3
            
        total_combinations = int(total_combinations * digit_spec_multiplier)
        
        if total_combinations < 1000:
            formatted_result = str(total_combinations)
        elif total_combinations < 1_000_000:
            formatted_result = f"{total_combinations:,}".replace(",", " ")
        else:
            power = len(str(total_combinations)) - 1
            base = total_combinations / (10 ** power)
            formatted_result = f"{base:.2f} × 10^{power}"
        
        formula_text = f"C = (21^{length // 2 + (length % 2)}) × (5^{length // 2})"
        if use_digits or use_special:
            formula_text += f" × {digit_spec_multiplier:.1f}"
            
        self.formula_label.setText(formula_text)
        self.result_label.setText(f"Всего комбинаций: {formatted_result}")
    
    def _update_pattern_combinations(self, length, use_upper, use_lower, use_digits, use_special):
        # Расчет для шаблонного алгоритма
        types_count = sum([use_upper, use_lower, use_digits, use_special])
        if types_count == 0:
            self.formula_label.setText("C = 0")
            self.result_label.setText("Выберите хотя бы один тип символов")
            return
            
        base_chars_per_type = length // types_count
        extra_chars = length % types_count
        
        formula_parts = []
        total_combinations = 1
        
        if use_upper:
            upper_count = base_chars_per_type + (1 if extra_chars > 0 else 0)
            extra_chars = max(0, extra_chars - 1)
            total_combinations *= 26 ** upper_count
            formula_parts.append(f"26^{upper_count}")
            
        if use_lower:
            lower_count = base_chars_per_type + (1 if extra_chars > 0 else 0)
            extra_chars = max(0, extra_chars - 1)
            total_combinations *= 26 ** lower_count
            formula_parts.append(f"26^{lower_count}")
            
        if use_digits:
            digits_count = base_chars_per_type + (1 if extra_chars > 0 else 0)
            extra_chars = max(0, extra_chars - 1)
            total_combinations *= 10 ** digits_count
            formula_parts.append(f"10^{digits_count}")
            
        if use_special:
            special_count = base_chars_per_type + (1 if extra_chars > 0 else 0)
            total_combinations *= 33 ** special_count
            formula_parts.append(f"33^{special_count}")
            
        if total_combinations < 1000:
            formatted_result = str(total_combinations)
        elif total_combinations < 1_000_000:
            formatted_result = f"{total_combinations:,}".replace(",", " ")
        else:
            power = len(str(total_combinations)) - 1
            base = total_combinations / (10 ** power)
            formatted_result = f"{base:.2f} × 10^{power}"
            
        self.formula_label.setText(f"C = {' × '.join(formula_parts)}")
        self.result_label.setText(f"Всего комбинаций: {formatted_result}")
    
    def _update_memorable_combinations(self, use_digits, use_special):
        # Расчет для запоминаемого алгоритма
        words_count = 32  
        
        total_combinations = words_count ** 2 
        
        formula_parts = [f"32^2"]
        
        if use_digits:
            total_combinations *= 10 ** 2
            formula_parts.append("10^2")
            
        if use_special:
            total_combinations *= 33
            formula_parts.append("33^1")
            
        if total_combinations < 1000:
            formatted_result = str(total_combinations)
        elif total_combinations < 1_000_000:
            formatted_result = f"{total_combinations:,}".replace(",", " ")
        else:
            power = len(str(total_combinations)) - 1
            base = total_combinations / (10 ** power)
            formatted_result = f"{base:.2f} × 10^{power}"
            
        self.formula_label.setText(f"C = {' × '.join(formula_parts)}")
        self.result_label.setText(f"Всего комбинаций: {formatted_result}") 