"""
Quotes Page for the Babbitt Quote Generator.
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QHeaderView,
    QTextEdit,
    QSplitter,
    QScrollArea,
)

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService


class QuotesPage(QWidget):
    """
    Page for viewing, editing, and searching quotes with a details panel.
    """
    edit_quote_requested = Signal(int)
    quote_deleted = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_quote_id = None
        self._init_ui()
        self.load_quotes()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side (Table)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(16)
        
        top_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search quotes by number, customer name, or company...")
        top_layout.addWidget(self.search_bar)
        
        top_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_quotes)
        top_layout.addWidget(refresh_btn)

        left_layout.addLayout(top_layout)

        self.quotes_table = QTableWidget()
        self.quotes_table.setObjectName("quotesTable")
        self.quotes_table.setColumnCount(5)
        self.quotes_table.setHorizontalHeaderLabels(["Quote #", "Customer", "Date", "Total", "Status"])
        
        header = self.quotes_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setStyleSheet("QHeaderView::section { border-right: 1px solid #d0d0d0; padding-left: 5px; }")
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.quotes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.quotes_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.quotes_table.setShowGrid(False)
        self.quotes_table.verticalHeader().setVisible(False)
        self.quotes_table.verticalHeader().setDefaultSectionSize(45)
        left_layout.addWidget(self.quotes_table)
        
        splitter.addWidget(left_widget)

        # Right side (Details Panel)
        details_panel = self._create_details_panel()
        splitter.addWidget(details_panel)
        
        splitter.setSizes([900, 400])
        main_layout.addWidget(splitter)

        self.search_bar.textChanged.connect(self._filter_quotes)
        self.quotes_table.itemSelectionChanged.connect(self._on_quote_selected)
        self.edit_quote_btn.clicked.connect(self._handle_edit_quote)
        self.delete_quote_btn.clicked.connect(self._handle_delete_quote)
        self.quotes_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.quotes_table.customContextMenuRequested.connect(self._show_quote_context_menu)

    def _create_details_panel(self):
        details_card = QFrame()
        details_card.setObjectName("detailsCard")
        
        card_layout = QVBoxLayout(details_card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(20)
        
        header_title = QLabel("Quote Details")
        header_title.setObjectName("detailsTitle")
        card_layout.addWidget(header_title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("detailsScrollArea")
        
        scroll_content = QWidget()
        self.details_layout = QVBoxLayout(scroll_content)
        
        self.details_quote_number = self._add_detail_to_layout("Quote #")
        self.details_customer = self._add_detail_to_layout("Customer")
        self.details_date = self._add_detail_to_layout("Date")
        self.details_total = self._add_detail_to_layout("Total")
        self.details_status = self._add_detail_to_layout("Status")
        
        self.details_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        card_layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.edit_quote_btn = QPushButton("Edit")
        self.edit_quote_btn.setProperty("class", "secondary")
        self.edit_quote_btn.setEnabled(False)
        button_layout.addWidget(self.edit_quote_btn)
        self.delete_quote_btn = QPushButton("Delete")
        self.delete_quote_btn.setProperty("class", "danger")
        self.delete_quote_btn.setEnabled(False)
        button_layout.addWidget(self.delete_quote_btn)
        button_layout.addStretch()
        card_layout.addLayout(button_layout)
        
        self.no_quote_selected_label = QLabel("Select a quote to see details.")
        self.no_quote_selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.no_quote_selected_label)
        
        self.scroll_area = scroll_area

        return details_card

    def _add_detail_to_layout(self, label_text, is_multiline=False):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(label_text)
        label.setObjectName("detailLabel")
        if is_multiline:
            value_widget = QTextEdit()
            value_widget.setReadOnly(True)
        else:
            value_widget = QLabel("—")
        value_widget.setObjectName("detailValue")
        layout.addWidget(label)
        layout.addWidget(value_widget)
        self.details_layout.addWidget(widget)
        return value_widget

    def _show_quote_context_menu(self, pos):
        """Show a context menu for the quotes table."""
        row_index = self.quotes_table.indexAt(pos).row()
        if row_index < 0:
            return  # Click was not on a row

        # Select the right-clicked row to ensure handlers have the correct context
        self.quotes_table.selectRow(row_index)

        menu = QMenu()
        edit_action = menu.addAction("Edit Quote")
        delete_action = menu.addAction("Delete Quote")

        # Execute menu and see which action was selected
        action = menu.exec(self.quotes_table.mapToGlobal(pos))

        if action == edit_action:
            self._handle_edit_quote()
        elif action == delete_action:
            self._handle_delete_quote()

    def _on_quote_selected(self):
        selected_items = self.quotes_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            quote_id_item = self.quotes_table.item(row, 0)
            if quote_id_item:
                self.selected_quote_id = quote_id_item.data(Qt.ItemDataRole.UserRole)
                self.edit_quote_btn.setEnabled(True)
                self.delete_quote_btn.setEnabled(True)
                self._update_details_panel(self.selected_quote_id)
        else:
            self._clear_details_panel()

    def _clear_details_panel(self):
        self.selected_quote_id = None
        self.edit_quote_btn.setEnabled(False)
        self.delete_quote_btn.setEnabled(False)
        self.no_quote_selected_label.setVisible(True)
        self.scroll_area.setVisible(False)
        self.details_quote_number.setText("—")
        self.details_customer.setText("—")
        self.details_date.setText("—")
        self.details_total.setText("—")
        self.details_status.setText("—")

    def _update_details_panel(self, quote_id):
        self.no_quote_selected_label.setVisible(False)
        self.scroll_area.setVisible(True)
        with SessionLocal() as db:
            details = QuoteService.get_full_quote_details(db, quote_id)
            if details:
                self.details_quote_number.setText(details.get("quote_number", "—"))
                self.details_customer.setText(details.get("customer", {}).get("name", "—"))
                date_created = details.get("date_created")
                self.details_date.setText(date_created.strftime("%Y-%m-%d") if date_created else "—")
                self.details_total.setText(f"${details.get('total', 0):,.2f}")
                self.details_status.setText(details.get("status", "—"))
                if isinstance(self.details_notes, QTextEdit):
                    self.details_notes.setPlainText(details.get("notes") or "")

    def load_quotes(self):
        """Loads all quotes from the database and populates the table."""
        self.search_bar.clear()  # Clear search to ensure all quotes are loaded
        with SessionLocal() as db:
            all_quotes = QuoteService.get_all_quotes_summary(db)
            self._populate_table(all_quotes)

    def _filter_quotes(self):
        """Filters quotes based on the search bar text."""
        search_term = self.search_bar.text()
        with SessionLocal() as db:
            filtered_quotes = QuoteService.search_quotes(db, search_term)
            self._populate_table(filtered_quotes)

    def _populate_table(self, quotes: list):
        """Populates the table with a given list of quotes."""
        self.quotes_table.setRowCount(0)
        for row, quote_summary in enumerate(quotes):
            self.quotes_table.insertRow(row)
            
            id_item = QTableWidgetItem(quote_summary["quote_number"])
            id_item.setData(Qt.ItemDataRole.UserRole, quote_summary["id"])
            
            items_to_add = [
                id_item,
                QTableWidgetItem(quote_summary["customer_name"]),
                QTableWidgetItem(quote_summary["date_created"]),
                QTableWidgetItem(f"${quote_summary.get('total', 0):,.2f}"),
                QTableWidgetItem(quote_summary.get("status", "N/A")),
            ]
            
            for col, item in enumerate(items_to_add):
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.quotes_table.setItem(row, col, item)

        if self.quotes_table.rowCount() > 0:
            self.quotes_table.selectRow(0)
        else:
            self._clear_details_panel()

    def _handle_edit_quote(self):
        if self.selected_quote_id:
            self.edit_quote_requested.emit(self.selected_quote_id)

    def _handle_delete_quote(self):
        if not self.selected_quote_id:
            return
            
        reply = QMessageBox.question(self, "Delete Quote", "Are you sure?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            with SessionLocal() as db:
                success = QuoteService.delete_quote(db, self.selected_quote_id)
                if success:
                    deleted_id = self.selected_quote_id
                    self.load_quotes()
                    self.quote_deleted.emit(deleted_id)
                else:
                    QMessageBox.warning(self, "Error", "Could not delete quote.") 