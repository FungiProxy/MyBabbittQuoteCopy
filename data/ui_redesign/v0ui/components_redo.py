"""
Reusable UI components for the BabbittQuote application
"""

from PySide6.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QComboBox, 
                               QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                               QFrame, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush
from styles import COLORS, FONTS, SPACING, RADIUS, get_button_style, get_input_style

class StatusBadge(QLabel):
    """A modern status badge component"""
    
    def __init__(self, text="", status_type="info", parent=None):
        super().__init__(text, parent)
        self.status_type = status_type
        self.setup_style()
    
    def setup_style(self):
        styles = {
            'draft': {
                'bg': COLORS['warning_light'],
                'text': COLORS['warning']
            },
            'active': {
                'bg': COLORS['success_light'],
                'text': COLORS['success']
            },
            'completed': {
                'bg': '#e0f2fe',
                'text': '#0369a1'
            },
            'cancelled': {
                'bg': '#fee2e2',
                'text': '#dc2626'
            }
        }
        
        style = styles.get(self.status_type, styles['draft'])
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {style['bg']};
                color: {style['text']};
                padding: {SPACING['xs']}px {SPACING['md']}px;
                border-radius: {RADIUS['full']}px;
                font-weight: {FONTS['weights']['semibold']};
                font-size: {FONTS['sizes']['xs']}px;
            }}
        """)
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class Card(QFrame):
    """A modern card container component"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_primary']};
                border-radius: {RADIUS['lg']}px;
                border: 1px solid {COLORS['border_light']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['2xl'], SPACING['2xl'], SPACING['2xl'], SPACING['2xl'])
        layout.setSpacing(SPACING['xl'])
        
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont(FONTS['family'], FONTS['sizes']['xl'], FONTS['weights']['semibold']))
            title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
            layout.addWidget(title_label)
        
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
    
    def add_widget(self, widget):
        """Add a widget to the card content"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add a layout to the card content"""
        self.content_layout.addLayout(layout)

class SearchBar(QWidget):
    """A modern search bar component"""
    
    search_changed = Signal(str)
    
    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setMinimumHeight(44)
        self.search_input.setStyleSheet(get_input_style())
        self.search_input.textChanged.connect(self.search_changed.emit)
        
        layout.addWidget(self.search_input)
    
    def get_text(self):
        return self.search_input.text()
    
    def clear(self):
        self.search_input.clear()

class PriceDisplay(QLabel):
    """A component for displaying prices with proper formatting"""
    
    def __init__(self, amount=0.0, currency="$", size="normal", parent=None):
        super().__init__(parent)
        self.currency = currency
        self.size = size
        self.set_amount(amount)
    
    def set_amount(self, amount):
        """Set the price amount"""
        self.amount = amount
        formatted_amount = f"{self.currency}{amount:,.2f}"
        self.setText(formatted_amount)
        self.update_style()
    
    def update_style(self):
        """Update the styling based on size"""
        sizes = {
            'small': FONTS['sizes']['base'],
            'normal': FONTS['sizes']['xl'],
            'large': FONTS['sizes']['4xl']
        }
        
        font_size = sizes.get(self.size, sizes['normal'])
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['success']};
                font-weight: {FONTS['weights']['bold']};
                font-size: {font_size}px;
            }}
        """)

class LoadingSpinner(QWidget):
    """A loading spinner component"""
    
    def __init__(self, size=32, parent=None):
        super().__init__(parent)
        self.size = size
        self.angle = 0
        self.setFixedSize(size, size)
        
        self.timer = None
    
    def start(self):
        """Start the spinning animation"""
        if not self.timer:
            from PySide6.QtCore import QTimer
            self.timer = QTimer()
            self.timer.timeout.connect(self.rotate)
            self.timer.start(50)  # Update every 50ms
    
    def stop(self):
        """Stop the spinning animation"""
        if self.timer:
            self.timer.stop()
            self.timer = None
    
    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 10) % 360
        self.update()
    
    def paintEvent(self, event):
        """Paint the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set up the pen
        pen = QPen(QColor(COLORS['primary']))
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # Draw the spinner arc
        rect = QRect(3, 3, self.size - 6, self.size - 6)
        painter.drawArc(rect, self.angle * 16, 120 * 16)

class EmptyState(QWidget):
    """A component for displaying empty states"""
    
    def __init__(self, title="No items found", description="", action_text="", parent=None):
        super().__init__(parent)
        self.setup_ui(title, description, action_text)
    
    def setup_ui(self, title, description, action_text):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(SPACING['lg'])
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont(FONTS['family'], FONTS['sizes']['2xl'], FONTS['weights']['semibold']))
        title_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont(FONTS['family'], FONTS['sizes']['base']))
            desc_label.setStyleSheet(f"color: {COLORS['text_muted']};")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Action button
        if action_text:
            from main import ModernButton
            action_btn = ModernButton(action_text, "primary")
            layout.addWidget(action_btn)
            self.action_button = action_btn

class Notification(QWidget):
    """A notification/toast component"""
    
    def __init__(self, message="", notification_type="info", parent=None):
        super().__init__(parent)
        self.notification_type = notification_type
        self.setup_ui(message)
        self.setup_animation()
    
    def setup_ui(self, message):
        self.setFixedHeight(60)
        self.setStyleSheet(self.get_notification_style())
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['md'], SPACING['lg'], SPACING['md'])
        
        # Message
        message_label = QLabel(message)
        message_label.setFont(QFont(FONTS['family'], FONTS['sizes']['base'], FONTS['weights']['medium']))
        message_label.setStyleSheet("color: white;")
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """)
        close_btn.clicked.connect(self.hide)
        layout.addWidget(close_btn)
    
    def get_notification_style(self):
        """Get the stylesheet based on notification type"""
        styles = {
            'success': f"background-color: {COLORS['success']};",
            'error': f"background-color: {COLORS['danger']};",
            'warning': f"background-color: {COLORS['warning']};",
            'info': f"background-color: {COLORS['primary']};"
        }
        
        base_style = f"""
            QWidget {{
                {styles.get(self.notification_type, styles['info'])}
                border-radius: {RADIUS['md']}px;
                border: none;
            }}
        """
        
        return base_style
    
    def setup_animation(self):
        """Setup slide-in animation"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def show_notification(self, parent_widget):
        """Show the notification with animation"""
        if parent_widget:
            # Position at top of parent
            parent_rect = parent_widget.rect()
            start_rect = QRect(parent_rect.x(), parent_rect.y() - self.height(), 
                             parent_rect.width(), self.height())
            end_rect = QRect(parent_rect.x(), parent_rect.y() + 20, 
                           parent_rect.width(), self.height())
            
            self.setGeometry(start_rect)
            self.show()
            
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            self.animation.start()
            
            # Auto-hide after 3 seconds
            from PySide6.QtCore import QTimer
            QTimer.singleShot(3000, self.hide)