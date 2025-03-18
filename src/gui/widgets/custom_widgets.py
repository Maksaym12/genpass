from PyQt5.QtWidgets import QSlider, QPushButton, QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QPen
from src.utils.styles import *

class AnimatedToggle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(TOGGLE_WIDTH, TOGGLE_HEIGHT)
        self._enabled = False
        self._circle_position = 4
        
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)
        
    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position
        
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
        
    def mousePressEvent(self, event):
        self._enabled = not self._enabled
        self.animation.setStartValue(self.circle_position)
        self.animation.setEndValue(TOGGLE_WIDTH - 24 if self._enabled else 4)
        self.animation.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(Qt.NoPen)
        
        if not self.isEnabled():
            painter.setBrush(QColor(120, 120, 120, 150))
        elif self._enabled:
            painter.setBrush(QColor(ACCENT_COLOR))
        else:
            painter.setBrush(QColor(BUTTON_COLOR))
            
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        
        if not self.isEnabled():
            painter.setBrush(QColor(200, 200, 200, 150))
        else:
            painter.setBrush(QColor(TEXT_COLOR))
            
        circle_size = 22
        y_pos = (self.height() - circle_size) // 2
        painter.drawEllipse(int(self.circle_position), y_pos, circle_size, circle_size)

class CustomSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 5px;
                background: {BUTTON_COLOR};
                margin: 0px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {ACCENT_COLOR};
                width: 21px;
                margin: -8px 0;
                border-radius: 10px;
            }}
            QSlider::sub-page:horizontal {{
                background: {ACCENT_COLOR};
                border-radius: 3px;
            }}
        """)

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._color_value = 0
        self.setFixedHeight(BUTTON_HEIGHT)
        self.setCursor(Qt.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"color_value")
        self._animation.setDuration(200)
        self.setStyleSheet(self._get_stylesheet())
        
    @pyqtProperty(int)
    def color_value(self):
        return self._color_value
        
    @color_value.setter
    def color_value(self, value):
        self._color_value = value
        self.setStyleSheet(self._get_stylesheet())
        
    def enterEvent(self, event):
        self._animation.setEndValue(100)
        self._animation.start()
        
    def leaveEvent(self, event):
        self._animation.setEndValue(0)
        self._animation.start()
        
    def _get_stylesheet(self):
        bg_color = self._mix_colors(BUTTON_COLOR, BUTTON_HOVER, self._color_value / 100)
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 7px;
                padding: 7px 13px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
            }}
        """
        
    def _mix_colors(self, color1, color2, factor):
        c1 = QColor(color1)
        c2 = QColor(color2)
        r = c1.red() + (c2.red() - c1.red()) * factor
        g = c1.green() + (c2.green() - c1.green()) * factor
        b = c1.blue() + (c2.blue() - c1.blue()) * factor
        return f"rgb({int(r)}, {int(g)}, {int(b)})"

class CloseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("✕", parent)
        self.setFixedSize(20, 20)
        self.setCursor(Qt.PointingHandCursor)
        self._update_stylesheet(False)
        
    def enterEvent(self, event):
        self._update_stylesheet(True)
        
    def leaveEvent(self, event):
        self._update_stylesheet(False)
        
    def _update_stylesheet(self, is_hover):
        bg_color = "#BE5A63" if is_hover else "#E06C75"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 10px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
                font-weight: bold;
            }}
        """)

class MinimizeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("−", parent)
        self.setFixedSize(20, 20)
        self.setCursor(Qt.PointingHandCursor)
        self._update_stylesheet(False)
        
    def enterEvent(self, event):
        self._update_stylesheet(True)
        
    def leaveEvent(self, event):
        self._update_stylesheet(False)
        
    def _update_stylesheet(self, is_hover):
        bg_color = "#3FA83F" if is_hover else "#4CC24C"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {TEXT_COLOR};
                border: none;
                border-radius: 10px;
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE_NORMAL}px;
                font-weight: bold;
            }}
        """) 