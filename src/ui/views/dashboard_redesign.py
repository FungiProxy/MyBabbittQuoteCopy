"""
Minimal Dashboard for MyBabbittQuote
Focus on actions, not analytics
"""

import logging
from typing import List, Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService

logger = logging.getLogger(__name__)


class DashboardRedesign(QWidget):
    """
    Dead simple dashboard - Recent quotes + quick actions.
    No analytics BS, just what you need to get work done.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.quote_service = QuoteService()
        self._setup_ui()
        self._load_recent_quotes()

    def _setup_ui(self):
        """Setup minimal UI - quick actions + recent quotes."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Quick actions row
        self._create_quick_actions()
        main_layout.addWidget(self.actions_frame)

        # Recent quotes
        self._create_recent_quotes_section()
        main_layout.addWidget(self.recent_frame)

    def _create_quick_actions(self):
        """Create action buttons that actually matter."""
        self.actions_frame = QFrame()
        self.actions_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QHBoxLayout(self.actions_frame)
        layout.setSpacing(15)

        # New Quote - main action
        new_quote_btn = QPushButton("+ New Quote")
        new_quote_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        # View All Quotes
        view_quotes_btn = QPushButton("View All Quotes")
        view_quotes_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """)

        # Manage Customers
        customers_btn = QPushButton("Customers")
        customers_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)

        layout.addWidget(new_quote_btn)
        layout.addWidget(view_quotes_btn)
        layout.addWidget(customers_btn)
        layout.addStretch()  # Push everything left

        # Connect signals
        new_quote_btn.clicked.connect(self._on_new_quote)
        view_quotes_btn.clicked.connect(self._on_view_quotes)
        customers_btn.clicked.connect(self._on_view_customers)

    def _create_recent_quotes_section(self):
        """Create recent quotes list - the only data that matters."""
        self.recent_frame = QFrame()
        layout = QVBoxLayout(self.recent_frame)
        layout.setSpacing(15)

        # Section header
        header = QLabel("Recent Quotes")
        header.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(header)

        # Quotes container with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarNever)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
            }
        """)

        self.quotes_container = QWidget()
        self.quotes_layout = QVBoxLayout(self.quotes_container)
        self.quotes_layout.setSpacing(0)
        self.quotes_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area.setWidget(self.quotes_container)
        layout.addWidget(scroll_area)

    def _load_recent_quotes(self):
        """Load and display recent quotes."""
        try:
            with SessionLocal() as db:
                # Use the existing get_dashboard_statistics method
                stats = self.quote_service.get_dashboard_statistics(db)
                recent_quotes = stats.get('recent_quotes', [])
                
                # Convert to the format expected by the UI
                formatted_quotes = [
                    {
                        'id': quote.get('quote_number', 'N/A'),
                        'customer_name': quote.get('customer', 'Unknown'),
                        'created_date': quote.get('date', 'N/A'),
                        'total_value': quote.get('total', 0),
                        'status': 'Draft'  # Default status
                    }
                    for quote in recent_quotes
                ]
                
                self._display_quotes(formatted_quotes)
        except Exception as e:
            logger.error(f"Error loading recent quotes: {e}")
            self._show_error_message("Failed to load recent quotes")

    def _display_quotes(self, quotes: List[Dict]):
        """Display quotes in the list."""
        # Clear existing quotes
        while self.quotes_layout.count():
            child = self.quotes_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not quotes:
            # Show empty state
            empty_label = QLabel("No recent quotes.\nClick 'New Quote' to get started!")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("""
                QLabel {
                    color: #6c757d;
                    font-size: 14px;
                    padding: 40px;
                    line-height: 1.5;
                }
            """)
            self.quotes_layout.addWidget(empty_label)
            return

        # Add quote items
        for quote in quotes:
            quote_item = self._create_quote_item(quote)
            self.quotes_layout.addWidget(quote_item)

        # Add stretch to push items to top
        self.quotes_layout.addStretch()

    def _create_quote_item(self, quote: Dict) -> QWidget:
        """Create a single quote list item."""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e9ecef;
                padding: 15px;
            }
            QFrame:hover {
                background-color: #f8f9fa;
            }
        """)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(0, 0, 0, 0)

        # Quote info
        info_layout = QVBoxLayout()

        # Quote number and customer
        title = QLabel(f"#{quote.get('id', 'N/A')} - {quote.get('customer_name', 'Unknown')}")
        title.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #2c3e50;
                font-size: 14px;
            }
        """)
        info_layout.addWidget(title)

        # Date and value on one line
        date_str = quote.get('created_date', 'N/A')
        value = quote.get('total_value', 0)
        details = QLabel(f"{date_str} • ${value:,.2f}")
        details.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
            }
        """)
        info_layout.addWidget(details)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Status badge
        status = quote.get('status', 'Draft')
        status_label = QLabel(status)
        
        status_colors = {
            'Draft': '#ffc107',
            'Sent': '#28a745', 
            'Approved': '#007bff',
            'Declined': '#dc3545'
        }
        
        color = status_colors.get(status, '#6c757d')
        status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(status_label)

        return item

    def _show_error_message(self, message: str):
        """Show error in quotes area."""
        # Clear existing content
        while self.quotes_layout.count():
            child = self.quotes_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        error_label = QLabel(f"⚠️ {message}")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-size: 14px;
                padding: 40px;
            }
        """)
        self.quotes_layout.addWidget(error_label)

    # Signal handlers that work with your MainWindowRedesign
    def _on_new_quote(self):
        """Handle new quote button click."""
        main_window = self._find_main_window()
        if main_window and hasattr(main_window, '_show_quote_creation'):
            main_window._show_quote_creation()

    def _on_view_quotes(self):
        """Handle view all quotes button click."""
        # For now, just show new quote since you don't have a quotes list view
        self._on_new_quote()

    def _on_view_customers(self):
        """Handle customers button click."""
        main_window = self._find_main_window()
        if main_window and hasattr(main_window, 'nav_list'):
            main_window.nav_list.setCurrentRow(2)  # Customers is index 2
    
    def _find_main_window(self):
        """Find the MainWindowRedesign instance."""
        widget = self
        while widget is not None:
            if hasattr(widget, 'nav_list') and hasattr(widget, '_show_quote_creation'):
                return widget
            widget = widget.parent()
        return None

    def refresh_data(self):
        """Refresh dashboard data."""
        self._load_recent_quotes()