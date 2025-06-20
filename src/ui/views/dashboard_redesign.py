"""
Redesigned Dashboard for MyBabbittQuote

Simplified dashboard focusing on essential business metrics without 
analytics/reports complexity. Clean card-based layout with key statistics.
"""

import logging
from typing import Dict, List

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
)

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService

logger = logging.getLogger(__name__)


class DashboardRedesign(QWidget):
    """
    Simplified dashboard for MyBabbittQuote focusing on core business metrics.
    
    Features:
    - Key statistics cards (quotes, revenue, customers)
    - Recent quotes list
    - Clean, professional layout
    - Auto-refresh capability
    """

    quote_loaded = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.quote_service = QuoteService()
        self._setup_ui()
        self._load_data()
        
        # Auto-refresh every 5 minutes
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(300000)  # 5 minutes

    def _setup_ui(self):
        """Set up the dashboard UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Statistics cards
        self._create_stats_section()
        main_layout.addWidget(self.stats_frame)
        
        # Recent activity
        self._create_recent_section()
        main_layout.addWidget(self.recent_frame)

    def _create_stats_section(self):
        """Create the statistics cards section."""
        self.stats_frame = QFrame()
        stats_layout = QGridLayout(self.stats_frame)
        stats_layout.setSpacing(20)
        
        # Create stat cards
        self.total_quotes_card = self._create_stat_card(
            "Total Quotes", "0", "This month", "📋"
        )
        self.quote_value_card = self._create_stat_card(
            "Quote Value", "$0", "Total pending", "💰"
        )
        self.active_customers_card = self._create_stat_card(
            "Active Customers", "0", "This quarter", "👥"
        )
        
        # Add cards to grid (responsive layout)
        stats_layout.addWidget(self.total_quotes_card, 0, 0)
        stats_layout.addWidget(self.quote_value_card, 0, 1)
        stats_layout.addWidget(self.active_customers_card, 0, 2)
        
        # Make columns equal width
        stats_layout.setColumnStretch(0, 1)
        stats_layout.setColumnStretch(1, 1)
        stats_layout.setColumnStretch(2, 1)

    def _create_stat_card(self, title: str, value: str, subtitle: str, icon: str) -> QFrame:
        """Create a statistics card widget."""
        card = QFrame()
        card.setProperty("class", "statCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with title and icon
        header_layout = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setProperty("class", "statTitle")

        icon_label = QLabel(icon)
        icon_label.setProperty("class", "statIcon")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(icon_label)

        layout.addLayout(header_layout)

        # Value
        value_label = QLabel(value)
        value_label.setProperty("class", "statValue")
        layout.addWidget(value_label)

        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setProperty("class", "statSubtitle")
        layout.addWidget(subtitle_label)

        # Store references for updating
        card.value_label = value_label
        card.subtitle_label = subtitle_label

        return card

    def _create_recent_section(self):
        """Create the recent quotes section."""
        self.recent_frame = QFrame()
        recent_layout = QVBoxLayout(self.recent_frame)
        
        # Section title
        title_label = QLabel("Recent Quotes")
        title_label.setObjectName("sectionTitle")
        recent_layout.addWidget(title_label)
        
        # Recent quotes container
        self.recent_quotes_container = QFrame()
        self.recent_quotes_container.setProperty("class", "card")
        
        self.recent_quotes_layout = QVBoxLayout(self.recent_quotes_container)
        
        # Placeholder
        placeholder = QLabel("Your recent quotes will appear here")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setProperty("class", "placeholderText")
        self.recent_quotes_layout.addWidget(placeholder)
        
        recent_layout.addWidget(self.recent_quotes_container)

    def _load_data(self):
        """Load dashboard data from the database."""
        try:
            with SessionLocal() as db:
                # Get statistics
                stats = self._get_dashboard_stats(db)
                self._update_stat_cards(stats)
                
                # Get recent quotes
                recent_quotes = self._get_recent_quotes(db)
                self._update_recent_quotes(recent_quotes)
                
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")

    def _get_dashboard_stats(self, db) -> Dict:
        """Get dashboard statistics."""
        try:
            # Use the correct method from QuoteService
            stats = self.quote_service.get_dashboard_statistics(db)
            
            return {
                'total_quotes': stats.get('total_quotes', 0),
                'total_value': stats.get('total_quote_value', 0.0),
                'active_customers': stats.get('total_customers', 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {
                'total_quotes': 0,
                'total_value': 0.0,
                'active_customers': 0
            }

    def _get_recent_quotes(self, db) -> List[Dict]:
        """Get recent quotes for display."""
        try:
            # Use the correct method from QuoteService
            stats = self.quote_service.get_dashboard_statistics(db)
            recent_quotes = stats.get('recent_quotes', [])
            
            # Convert to the format expected by the UI
            return [
                {
                    'db_id': quote.get('id'),
                    'quote_number': quote.get('quote_number', 'N/A'),
                    'customer_name': quote.get('customer', 'Unknown'),
                    'created_date': quote.get('date', 'N/A'),
                    'total_value': quote.get('total', 0),
                    'status': 'Draft'  # Default status since it's not in the data
                }
                for quote in recent_quotes
            ]
            
        except Exception as e:
            logger.error(f"Error getting recent quotes: {e}")
            return []

    def _update_stat_cards(self, stats: Dict):
        """Update the statistics cards with new data."""
        # Update total quotes
        self.total_quotes_card.value_label.setText(str(stats['total_quotes']))
        
        # Update quote value
        value_formatted = f"${stats['total_value']:,.2f}"
        self.quote_value_card.value_label.setText(value_formatted)
        
        # Update active customers
        self.active_customers_card.value_label.setText(str(stats['active_customers']))

    def _update_recent_quotes(self, quotes: List[Dict]):
        """Update the recent quotes section."""
        # Clear existing items
        for i in reversed(range(self.recent_quotes_layout.count())):
            child = self.recent_quotes_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        if not quotes:
            # Show placeholder
            placeholder = QLabel("No recent quotes found")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setProperty("class", "placeholderText")
            self.recent_quotes_layout.addWidget(placeholder)
        else:
            # Add quote items
            for quote in quotes:
                quote_item = self._create_quote_item(quote)
                self.recent_quotes_layout.addWidget(quote_item)

    def _create_quote_item(self, quote: Dict) -> QFrame:
        """Create a recent quote item widget."""
        item = QFrame()
        item.setProperty("class", "quoteItemCard")

        layout = QHBoxLayout(item)
        
        # Details
        details_layout = QVBoxLayout()
        quote_id_label = QLabel(f"Quote #{quote['quote_number']}")
        quote_id_label.setProperty("class", "quoteItemTitle")
        
        customer_label = QLabel(quote['customer_name'])
        customer_label.setProperty("class", "quoteItemDetails")
        
        details_layout.addWidget(quote_id_label)
        details_layout.addWidget(customer_label)
        layout.addLayout(details_layout)
        
        layout.addStretch()
        
        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        load_button = QPushButton("Load")
        load_button.setProperty("class", "button-secondary")
        load_button.clicked.connect(lambda: self._load_quote(quote['db_id']))
        
        delete_button = QPushButton("Delete")
        delete_button.setProperty("class", "button-danger")
        delete_button.clicked.connect(lambda: self._delete_quote(quote['db_id']))
        
        actions_layout.addWidget(load_button)
        actions_layout.addWidget(delete_button)
        
        layout.addLayout(actions_layout)

        return item

    def _load_quote(self, quote_id: int):
        """Load a quote and emit a signal."""
        logger.info(f"Loading quote {quote_id}")
        try:
            with SessionLocal() as db:
                quote_details = self.quote_service.get_full_quote_details(db, quote_id)
                if quote_details:
                    self.quote_loaded.emit(quote_details)
                else:
                    QMessageBox.warning(self, "Not Found", f"Quote with ID {quote_id} not found.")
        except Exception as e:
            logger.error(f"Error loading quote {quote_id}: {e}")
            QMessageBox.critical(self, "Error", "Could not load quote.")

    def _delete_quote(self, quote_id: int):
        """Delete a quote."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete quote {quote_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            logger.info(f"Deleting quote {quote_id}")
            try:
                with SessionLocal() as db:
                    success = self.quote_service.delete_quote(db, quote_id)
                    if success:
                        QMessageBox.information(self, "Success", f"Quote {quote_id} deleted.")
                        self.refresh_data()
                    else:
                        QMessageBox.warning(self, "Not Found", f"Quote with ID {quote_id} not found.")
            except Exception as e:
                logger.error(f"Error deleting quote {quote_id}: {e}")
                QMessageBox.critical(self, "Error", "Could not delete quote.")

    def refresh_data(self):
        """Refresh dashboard data."""
        logger.info("Refreshing dashboard data...")
        self._load_data()
        logger.info("Dashboard data refreshed")

    def showEvent(self, event):
        """Handle widget show event."""
        super().showEvent(event)
        # Refresh data when dashboard becomes visible
        self.refresh_data()