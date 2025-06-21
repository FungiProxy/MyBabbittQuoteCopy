"""
Professional Dashboard Implementation - MyBabbittQuote

Restores the beautiful card-based dashboard design with enhanced styling.
This creates the professional appearance shown in your desired screenshot.

File: src/ui/views/dashboard_enhanced.py
"""

import logging
from typing import Dict, List

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect,
)
from PySide6.QtGui import QColor

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService

logger = logging.getLogger(__name__)


class StatisticsCard(QFrame):
    """
    Professional statistics card widget that matches your previous design.
    Creates the clean white cards with proper spacing and typography.
    """
    
    def __init__(self, title: str, value: str, subtitle: str, icon: str, parent=None):
        super().__init__(parent)
        self._setup_card_styling()
        self._create_layout(title, value, subtitle, icon)
    
    def _setup_card_styling(self):
        """Apply professional card styling."""
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 0px;
                margin: 8px;
            }
            QFrame:hover {
                border-color: #d1d5db;
                /* box-shadow removed: use QGraphicsDropShadowEffect in code */
            }
        """)
        self.setFixedHeight(120)
        self.setMinimumWidth(200)
        self.apply_shadow(self)
    
    @staticmethod
    def apply_shadow(widget, blur_radius=24, x_offset=0, y_offset=6, color="#000000", alpha=0.4):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(blur_radius)
        effect.setOffset(x_offset, y_offset)
        qcolor = QColor(color)
        qcolor.setAlphaF(alpha)
        effect.setColor(qcolor)
        widget.setGraphicsEffect(effect)
    
    def _create_layout(self, title: str, value: str, subtitle: str, icon: str):
        """Create the card layout with proper hierarchy."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Header with title and icon
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 13px;
                font-weight: 500;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        # Icon
        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-size: 18px;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.icon_label)
        layout.addLayout(header_layout)
        
        # Main value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("""
            QLabel {
                color: #111827;
                font-size: 28px;
                font-weight: 700;
                margin: 0px;
                padding: 0px;
                line-height: 1.0;
            }
        """)
        layout.addWidget(self.value_label)
        
        # Subtitle
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 12px;
                font-weight: 400;
                margin: 0px;
                padding: 0px;
            }
        """)
        layout.addWidget(self.subtitle_label)
    
    def update_value(self, value: str):
        """Update the card's main value."""
        self.value_label.setText(value)
    
    def update_subtitle(self, subtitle: str):
        """Update the card's subtitle."""
        self.subtitle_label.setText(subtitle)


class RecentQuotesSection(QFrame):
    """Professional recent quotes section with proper styling."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_styling()
        self._create_layout()
    
    def _setup_styling(self):
        """Apply section styling."""
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                margin: 8px;
            }
        """)
        self.setMinimumHeight(200)
    
    def _create_layout(self):
        """Create the section layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Section title
        title_label = QLabel("Recent Quotes")
        title_label.setStyleSheet("""
            QLabel {
                color: #111827;
                font-size: 18px;
                font-weight: 600;
                margin: 0px;
                padding: 0px;
            }
        """)
        layout.addWidget(title_label)
        
        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)
        
        # Empty state placeholder
        self.empty_label = QLabel("No recent quotes found")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-size: 14px;
                font-style: italic;
                padding: 40px;
                margin: 0px;
            }
        """)
        self.content_layout.addWidget(self.empty_label)
        
        layout.addLayout(self.content_layout)
    
    def update_quotes(self, quotes: List[Dict]):
        """Update the quotes display."""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        if not quotes:
            # Show empty state
            self.empty_label = QLabel("No recent quotes found")
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.empty_label.setStyleSheet("""
                QLabel {
                    color: #9ca3af;
                    font-size: 14px;
                    font-style: italic;
                    padding: 40px;
                    margin: 0px;
                }
            """)
            self.content_layout.addWidget(self.empty_label)
        else:
            # Add quote items
            for quote in quotes[:5]:  # Show max 5 recent quotes
                quote_item = self._create_quote_item(quote)
                self.content_layout.addWidget(quote_item)
    
    def _create_quote_item(self, quote: Dict) -> QWidget:
        """Create a quote item display."""
        item_frame = QFrame()
        item_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border: 1px solid #f3f4f6;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
            }
            QFrame:hover {
                background-color: #f3f4f6;
            }
        """)
        
        layout = QHBoxLayout(item_frame)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Quote info
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)
        
        # Quote number and customer
        main_text = f"Quote #{quote.get('quote_number', 'N/A')} - {quote.get('customer_name', 'Unknown')}"
        main_label = QLabel(main_text)
        main_label.setStyleSheet("""
            QLabel {
                color: #111827;
                font-size: 13px;
                font-weight: 500;
                margin: 0px;
            }
        """)
        
        # Date
        date_text = quote.get('date_created', 'Unknown date')
        date_label = QLabel(str(date_text))
        date_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 11px;
                margin: 0px;
            }
        """)
        
        info_layout.addWidget(main_label)
        info_layout.addWidget(date_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        # Value
        value_text = f"${quote.get('total_value', 0):,.2f}"
        value_label = QLabel(value_text)
        value_label.setStyleSheet("""
            QLabel {
                color: #059669;
                font-size: 13px;
                font-weight: 600;
                margin: 0px;
            }
        """)
        layout.addWidget(value_label)
        
        return item_frame


class ProfessionalDashboard(QWidget):
    """
    Professional dashboard that restores your beautiful card-based design.
    Matches the appearance from your desired screenshot.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quote_service = QuoteService()
        self._setup_ui()
        self._load_initial_data()
        
        # Auto-refresh every 30 seconds for demo purposes
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._load_initial_data)
        self.refresh_timer.start(30000)
    
    def _setup_ui(self):
        """Set up the professional dashboard UI."""
        # Main layout with proper spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)
        
        # Statistics cards section
        self._create_statistics_section()
        main_layout.addWidget(self.stats_container)
        
        # Recent quotes section
        self.recent_quotes_section = RecentQuotesSection()
        main_layout.addWidget(self.recent_quotes_section)
        
        # Add stretch to push content to top
        main_layout.addStretch()
    
    def _create_statistics_section(self):
        """Create the statistics cards section."""
        self.stats_container = QWidget()
        stats_layout = QGridLayout(self.stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(16)
        
        # Create the three main statistic cards
        self.total_quotes_card = StatisticsCard(
            "Total Quotes", "0", "This month", "📋"
        )
        self.quote_value_card = StatisticsCard(
            "Quote Value", "$0.00", "Total pending", "💰"
        )
        self.active_customers_card = StatisticsCard(
            "Active Customers", "0", "This quarter", "👥"
        )
        
        # Add cards to grid layout
        stats_layout.addWidget(self.total_quotes_card, 0, 0)
        stats_layout.addWidget(self.quote_value_card, 0, 1)
        stats_layout.addWidget(self.active_customers_card, 0, 2)
        
        # Ensure equal column widths
        stats_layout.setColumnStretch(0, 1)
        stats_layout.setColumnStretch(1, 1)
        stats_layout.setColumnStretch(2, 1)
    
    def _load_initial_data(self):
        """Load dashboard data from the database."""
        try:
            with SessionLocal() as db:
                # Get basic statistics
                stats = self._get_dashboard_statistics(db)
                self._update_statistics_cards(stats)
                
                # Get recent quotes
                recent_quotes = self._get_recent_quotes(db)
                self.recent_quotes_section.update_quotes(recent_quotes)
                
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            # Show default values on error
            self._show_default_values()
    
    def _get_dashboard_statistics(self, db) -> Dict:
        """Get dashboard statistics from the database."""
        try:
            # Use the quote service to get statistics
            total_quotes = self.quote_service.get_total_quotes_count(db) or 0
            total_value = self.quote_service.get_total_quotes_value(db) or 0.0
            customer_count = self.quote_service.get_customer_count(db) or 0
            
            return {
                'total_quotes': total_quotes,
                'total_value': total_value,
                'customer_count': customer_count
            }
        except Exception as e:
            logger.error(f"Error fetching statistics: {e}")
            return {'total_quotes': 0, 'total_value': 0.0, 'customer_count': 0}
    
    def _get_recent_quotes(self, db) -> List[Dict]:
        """Get recent quotes from the database."""
        try:
            return self.quote_service.get_recent_quotes(db, limit=5) or []
        except Exception as e:
            logger.error(f"Error fetching recent quotes: {e}")
            return []
    
    def _update_statistics_cards(self, stats: Dict):
        """Update the statistics cards with new data."""
        # Update total quotes
        self.total_quotes_card.update_value(str(stats['total_quotes']))
        
        # Update quote value with proper formatting
        value_formatted = f"${stats['total_value']:,.2f}"
        self.quote_value_card.update_value(value_formatted)
        
        # Update customer count
        self.active_customers_card.update_value(str(stats['customer_count']))
    
    def _show_default_values(self):
        """Show default values when data loading fails."""
        self.total_quotes_card.update_value("0")
        self.quote_value_card.update_value("$0.00")
        self.active_customers_card.update_value("0")
        
        # Show empty recent quotes
        self.recent_quotes_section.update_quotes([])
    
    def refresh_data(self):
        """Public method to refresh dashboard data."""
        self._load_initial_data()