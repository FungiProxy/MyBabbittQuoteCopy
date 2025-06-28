"""
Modern UI Components for MyBabbittQuote

Reusable components with consistent styling and behavior.
"""

from PySide6.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QComboBox, 
                               QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                               QFrame, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush

# Import styling from centralized theme system
from ..theme import (
    COLORS, FONTS, SPACING, RADIUS,
    get_status_badge_style, get_notification_style
)


class StatusBadge(QLabel):
    """
    A modern status badge component for displaying status information.
    
    Usage:
        badge = StatusBadge("Draft", "draft")
        badge = StatusBadge("Active", "active")
        badge = StatusBadge("Completed", "completed")
        badge = StatusBadge("Cancelled", "cancelled")
    """
    
    def __init__(self, text="", status_type="info", parent=None):
        super().__init__(text, parent)
        self.status_type = status_type
        self.setup_style()
    
    def setup_style(self):
        """Apply styling based on status type"""
        self.setStyleSheet(get_status_badge_style(self.status_type))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def set_status(self, status_type):
        """Update the status type and styling"""
        self.status_type = status_type
        self.setup_style()
    
    def set_text(self, text):
        """Update the badge text"""
        self.setText(text)


class Card(QFrame):
    """
    A modern card container component for organizing content.
    
    Usage:
        card = Card("Quote Details")
        card.add_widget(some_widget)
        card.add_layout(some_layout)
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the card UI"""
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
    
    def set_title(self, title):
        """Update the card title"""
        self.title = title
        # Recreate the UI to update the title
        self.setup_ui()
    
    def clear_content(self):
        """Clear all content from the card"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class SearchBar(QWidget):
    """
    A modern search bar component with real-time search functionality.
    
    Usage:
        search_bar = SearchBar("Search quotes...")
        search_bar.search_changed.connect(on_search_changed)
    """
    
    search_changed = Signal(str)
    
    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder):
        """Initialize the search bar UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setMinimumHeight(44)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                background-color: {COLORS['bg_primary']};
                font-size: {FONTS['sizes']['lg']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
            }}
            QLineEdit:focus {{
                border-color: {COLORS['primary']};
                outline: none;
            }}
            QLineEdit:hover {{
                border-color: #cbd5e1;
            }}
        """)
        self.search_input.textChanged.connect(self.search_changed.emit)
        
        layout.addWidget(self.search_input)
    
    def get_text(self):
        """Get the current search text"""
        return self.search_input.text()
    
    def clear(self):
        """Clear the search input"""
        self.search_input.clear()
    
    def set_placeholder(self, placeholder):
        """Update the placeholder text"""
        self.search_input.setPlaceholderText(placeholder)
    
    def set_text(self, text):
        """Set the search text programmatically"""
        self.search_input.setText(text)


class PriceDisplay(QLabel):
    """
    A component for displaying prices with proper formatting.
    
    Usage:
        price = PriceDisplay(425.00, "$", "normal")
        price.set_amount(500.00)
    """
    
    def __init__(self, amount=0.0, currency="$", size="normal", parent=None):
        super().__init__(parent)
        self.currency = currency
        self.display_size = size
        self.set_amount(amount)
    
    def set_amount(self, amount):
        """Set the price amount and update display"""
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
        
        font_size = sizes.get(self.display_size, sizes['normal'])
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['success']};
                font-weight: {FONTS['weights']['bold']};
                font-size: {font_size}px;
                font-family: {FONTS['family']};
            }}
        """)
    
    def set_currency(self, currency):
        """Update the currency symbol"""
        self.currency = currency
        self.set_amount(self.amount)
    
    def set_size(self, size):
        """Update the display size"""
        self.display_size = size
        self.update_style()
    
    def get_amount(self):
        """Get the current amount"""
        return self.amount


class LoadingSpinner(QWidget):
    """
    A loading spinner component for indicating async operations.
    
    Usage:
        spinner = LoadingSpinner(32)
        spinner.start()
        # ... do work ...
        spinner.stop()
    """
    
    def __init__(self, size=32, parent=None):
        super().__init__(parent)
        self.spinner_size = size
        self.angle = 0
        self.setFixedSize(size, size)
        
        self.timer = None
    
    def start(self):
        """Start the spinning animation"""
        if not self.timer:
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
        rect = QRect(3, 3, self.spinner_size - 6, self.spinner_size - 6)
        painter.drawArc(rect, self.angle * 16, 120 * 16)
    
    def set_size(self, size):
        """Update the spinner size"""
        self.spinner_size = size
        self.setFixedSize(size, size)
        self.update()


class EmptyState(QWidget):
    """
    A component for displaying empty states when lists or tables are empty.
    
    Usage:
        empty = EmptyState("No quotes found", "Create your first quote to get started", "New Quote")
        empty.action_button.clicked.connect(create_quote)
    """
    
    def __init__(self, title="No items found", description="", action_text="", parent=None):
        super().__init__(parent)
        self.setup_ui(title, description, action_text)
    
    def setup_ui(self, title, description, action_text):
        """Initialize the empty state UI"""
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
            # Create a simple button for now - will be replaced with ModernButton in Phase 3
            action_btn = QPushButton(action_text)
            action_btn.setMinimumHeight(40)
            action_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary']};
                    color: white;
                    border: none;
                    border-radius: {RADIUS['md']}px;
                    padding: {SPACING['md']}px {SPACING['2xl']}px;
                    font-weight: {FONTS['weights']['semibold']};
                    font-size: {FONTS['sizes']['base']}px;
                    font-family: {FONTS['family']};
                }}
                QPushButton:hover {{
                    background-color: #1d4ed8;
                }}
                QPushButton:pressed {{
                    background-color: #1e40af;
                }}
            """)
            layout.addWidget(action_btn)
            self.action_button = action_btn
    
    def set_title(self, title):
        """Update the empty state title"""
        # Find and update the title label
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget() and isinstance(item.widget(), QLabel):
                if item.widget().font().weight() == FONTS['weights']['semibold']:
                    item.widget().setText(title)
                    break
    
    def set_description(self, description):
        """Update the empty state description"""
        # Find and update the description label
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget() and isinstance(item.widget(), QLabel):
                if item.widget().font().weight() == FONTS['weights']['normal']:
                    item.widget().setText(description)
                    break
    
    def set_action_text(self, action_text):
        """Update the action button text"""
        if hasattr(self, 'action_button'):
            self.action_button.setText(action_text)


class Notification(QWidget):
    """
    A notification/toast component for displaying temporary messages.
    
    Usage:
        notification = Notification("Quote saved successfully!", "success")
        notification.show_notification(parent_widget)
    """
    
    def __init__(self, message="", notification_type="info", parent=None):
        super().__init__(parent)
        self.notification_type = notification_type
        self.setup_ui(message)
        self.setup_animation()
    
    def setup_ui(self, message):
        """Initialize the notification UI"""
        self.setFixedHeight(60)
        self.setStyleSheet(get_notification_style(self.notification_type))
        
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
            QTimer.singleShot(3000, self.hide)
    
    def set_message(self, message):
        """Update the notification message"""
        # Find and update the message label
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget() and isinstance(item.widget(), QLabel):
                item.widget().setText(message)
                break
    
    def set_type(self, notification_type):
        """Update the notification type and styling"""
        self.notification_type = notification_type
        self.setStyleSheet(get_notification_style(notification_type)) 