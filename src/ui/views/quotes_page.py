"""
Quotes Page for the Babbitt Quote Generator.
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService


class QuotesPage(QWidget):
    """
    Page for viewing, editing, and deleting quotes.
    """
    edit_quote_requested = Signal(int)
    quote_deleted = Signal(int)  # Signal emitted when a quote is deleted

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Quotes")
        
        self._init_ui()
        self.load_quotes()

    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        title = QLabel("All Quotes")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        self.quotes_table = QTableWidget()
        self.quotes_table.setColumnCount(6)
        self.quotes_table.setHorizontalHeaderLabels([
            "Quote #", "Customer", "Date", "Total", "Status", "Actions"
        ])
        header = self.quotes_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.quotes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.quotes_table)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_quotes)
        layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def load_quotes(self):
        """Load quotes from the database into the table."""
        try:
            with SessionLocal() as db:
                quotes = QuoteService.get_all_quotes_summary(db)
                self.quotes_table.setRowCount(0)
                for row, quote in enumerate(quotes):
                    self.quotes_table.insertRow(row)
                    
                    id_item = QTableWidgetItem(quote["quote_number"])
                    id_item.setData(Qt.ItemDataRole.UserRole, quote["id"])
                    
                    self.quotes_table.setItem(row, 0, id_item)
                    self.quotes_table.setItem(row, 1, QTableWidgetItem(quote["customer_name"]))
                    self.quotes_table.setItem(row, 2, QTableWidgetItem(quote["date_created"]))
                    self.quotes_table.setItem(row, 3, QTableWidgetItem(f"${quote.get('total', 0):,.2f}"))
                    self.quotes_table.setItem(row, 4, QTableWidgetItem(quote.get("status", "N/A")))
                    
                    # Actions
                    edit_btn = QPushButton("Edit")
                    delete_btn = QPushButton("Delete")
                    edit_btn.clicked.connect(lambda _, r=row: self._edit_quote(r))
                    delete_btn.clicked.connect(lambda _, r=row: self._delete_quote(r))

                    actions_widget = QWidget()
                    actions_layout = QHBoxLayout(actions_widget)
                    actions_layout.addWidget(edit_btn)
                    actions_layout.addWidget(delete_btn)
                    actions_layout.setContentsMargins(0, 0, 0, 0)
                    self.quotes_table.setCellWidget(row, 5, actions_widget)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load quotes: {e}")

    def _edit_quote(self, row):
        """Handle edit quote button click."""
        item = self.quotes_table.item(row, 0)
        if item:
            quote_id = item.data(Qt.ItemDataRole.UserRole)
            self.edit_quote_requested.emit(quote_id)

    def _delete_quote(self, row):
        """Handle delete quote button click."""
        item = self.quotes_table.item(row, 0)
        if not item:
            return
            
        quote_id = item.data(Qt.ItemDataRole.UserRole)
        quote_number = item.text()
        
        reply = QMessageBox.question(
            self,
            "Delete Quote",
            f"Are you sure you want to delete quote {quote_number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with SessionLocal() as db:
                    success = QuoteService.delete_quote(db, quote_id)
                    if success:
                        QMessageBox.information(self, "Success", "Quote deleted.")
                        self.load_quotes()
                        self.quote_deleted.emit(quote_id)
                    else:
                        QMessageBox.warning(self, "Error", "Could not delete quote.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete quote: {e}") 