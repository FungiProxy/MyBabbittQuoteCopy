from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QStackedWidget, QDateEdit, QFormLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from src.ui.product_selection_dialog import ProductSelectionDialog

class QuoteCreationPage(QWidget):
    """
    Multi-step Quote Creation UI matching the new design.
    Step 1: Customer Info
    Step 2: Product Selection (placeholder for now)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0  # 0: Customer Info, 1: Product Selection
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Title and Save Draft button
        header_layout = QHBoxLayout()
        title_label = QLabel("Quote Creation")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.save_draft_btn = QPushButton("Save Draft")
        self.save_draft_btn.setFixedWidth(120)
        header_layout.addWidget(self.save_draft_btn)
        self.main_layout.addLayout(header_layout)

        # Card/Panel for the form
        self.card = QFrame()
        self.card.setObjectName("quoteCreationCard")
        self.card.setStyleSheet("QFrame#quoteCreationCard { background: white; border-radius: 10px; border: 1px solid #e0e0e0; }")
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(30, 30, 30, 30)
        self.card_layout.setSpacing(20)

        # Subtitle
        self.subtitle = QLabel()
        self.subtitle.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.card_layout.addWidget(self.subtitle)
        self.desc = QLabel()
        self.desc.setStyleSheet("color: #888; font-size: 15px;")
        self.card_layout.addWidget(self.desc)

        # Stepper
        self.stepper_layout = QHBoxLayout()
        self.card_layout.addLayout(self.stepper_layout)

        # Stacked widget for steps
        self.steps_stack = QStackedWidget()
        self.card_layout.addWidget(self.steps_stack)

        # Step 1: Customer Info
        self.customer_info_widget = QWidget()
        customer_info_layout = QVBoxLayout(self.customer_info_widget)
        form_layout = QHBoxLayout()
        left_form = QFormLayout()
        right_form = QFormLayout()
        left_form.setLabelAlignment(Qt.AlignLeft)
        right_form.setLabelAlignment(Qt.AlignLeft)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        left_form.addRow("Customer Name", self.customer_name)
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter email address")
        left_form.addRow("Email", self.email)
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Enter phone number")
        left_form.addRow("Phone", self.phone)
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Enter company name")
        right_form.addRow("Company Name", self.company_name)
        self.quote_reference = QLineEdit("BQ-2025-7020")
        right_form.addRow("Quote Reference", self.quote_reference)
        self.quote_date = QDateEdit(QDate.currentDate())
        self.quote_date.setCalendarPopup(True)
        right_form.addRow("Quote Date", self.quote_date)
        self.expiration_date = QDateEdit(QDate.currentDate().addDays(30))
        self.expiration_date.setCalendarPopup(True)
        right_form.addRow("Expiration Date", self.expiration_date)
        form_layout.addLayout(left_form)
        form_layout.addSpacing(40)
        form_layout.addLayout(right_form)
        customer_info_layout.addLayout(form_layout)
        # Next Step button
        next_btn_layout = QHBoxLayout()
        next_btn_layout.addStretch()
        self.next_step_btn = QPushButton("Next Step →")
        self.next_step_btn.setFixedWidth(140)
        next_btn_layout.addWidget(self.next_step_btn)
        customer_info_layout.addLayout(next_btn_layout)
        self.steps_stack.addWidget(self.customer_info_widget)

        # Step 2: Product Selection (matches screenshot)
        self.product_selection_widget = QWidget()
        product_selection_layout = QVBoxLayout(self.product_selection_widget)
        product_selection_layout.setSpacing(20)

        # Quote Items header and Add Product button
        header_layout = QHBoxLayout()
        quote_items_label = QLabel("Quote Items")
        quote_items_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(quote_items_label)
        header_layout.addStretch()
        self.add_product_btn = QPushButton("+ Add Product")
        self.add_product_btn.setStyleSheet("background-color: #0056d6; color: white; font-weight: bold; padding: 8px 24px; border-radius: 6px; font-size: 16px;")
        self.add_product_btn.setFixedHeight(40)
        header_layout.addWidget(self.add_product_btn)
        product_selection_layout.addLayout(header_layout)

        # Card for quote items (empty state)
        quote_items_card = QFrame()
        quote_items_card.setStyleSheet("QFrame { background: #fff; border: 1px solid #e0e0e0; border-radius: 10px; }")
        quote_items_card.setMinimumHeight(220)
        card_layout = QVBoxLayout(quote_items_card)
        card_layout.setAlignment(Qt.AlignCenter)
        # Empty state icon and message
        icon_label = QLabel("\U0001F4E6")  # 📦
        icon_label.setStyleSheet("font-size: 48px; color: #90b4fa; margin-bottom: 10px;")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        no_products_label = QLabel("No Products Added")
        no_products_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 8px;")
        no_products_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(no_products_label)
        hint_label = QLabel('Click the "Add Product" button to start adding products to your quote.')
        hint_label.setStyleSheet("font-size: 15px; color: #888;")
        hint_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(hint_label)
        product_selection_layout.addWidget(quote_items_card)

        # Navigation buttons (Previous Step, Next Step)
        nav_btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("Previous Step")
        self.back_btn.setStyleSheet("padding: 10px 24px; font-size: 15px; border-radius: 6px; background: #fff; border: 1px solid #e0e0e0;")
        self.back_btn.setFixedWidth(140)
        nav_btn_layout.addWidget(self.back_btn)
        nav_btn_layout.addStretch()
        self.next_step_btn2 = QPushButton("Next Step  →")
        self.next_step_btn2.setStyleSheet("padding: 10px 24px; font-size: 15px; border-radius: 6px; background: #1976d2; color: #fff; font-weight: bold;")
        self.next_step_btn2.setFixedWidth(140)
        nav_btn_layout.addWidget(self.next_step_btn2)
        product_selection_layout.addLayout(nav_btn_layout)
        self.steps_stack.addWidget(self.product_selection_widget)

        self.main_layout.addWidget(self.card)
        self.main_layout.addStretch()

        # Footer
        footer_layout = QHBoxLayout()
        footer_left = QLabel("Babbitt International Inc.")
        footer_right = QLabel("© 2025 All rights reserved")
        footer_layout.addWidget(footer_left)
        footer_layout.addStretch()
        footer_layout.addWidget(footer_right)
        self.main_layout.addLayout(footer_layout)

        self._update_step()
        self.next_step_btn.clicked.connect(self._go_to_product_selection)
        self.back_btn.clicked.connect(self._go_to_customer_info)
        self.add_product_btn.clicked.connect(self._open_product_dialog)

    def _add_step_label(self, layout, number, text, active=False):
        step = QLabel(f"{number}")
        step.setFixedSize(28, 28)
        step.setAlignment(Qt.AlignCenter)
        step.setStyleSheet(f"border-radius: 14px; background: {'#e0e7ff' if active else '#f3f4f6'}; color: {'#2563eb' if active else '#888'}; font-weight: bold;")
        label = QLabel(text)
        label.setStyleSheet(f"color: {'#2563eb' if active else '#888'}; font-weight: {'bold' if active else 'normal'}; margin-left: 6px;")
        stepper_item = QHBoxLayout()
        stepper_item.addWidget(step)
        stepper_item.addWidget(label)
        layout.addLayout(stepper_item)
        if number < 3:
            arrow = QLabel("→")
            arrow.setStyleSheet("color: #bbb; font-size: 18px; margin: 0 12px;")
            layout.addWidget(arrow)

    def _update_step(self):
        # Clear stepper layout
        while self.stepper_layout.count():
            item = self.stepper_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
        # Add stepper with correct active step
        self._add_step_label(self.stepper_layout, 1, "Customer Info", active=(self.current_step == 0))
        self._add_step_label(self.stepper_layout, 2, "Product Selection", active=(self.current_step == 1))
        self._add_step_label(self.stepper_layout, 3, "Review & Finalize", active=False)
        # Update subtitle and description
        if self.current_step == 0:
            self.subtitle.setText("Create New Quote")
            self.desc.setText("Fill in the details to generate a new sales quote")
            self.steps_stack.setCurrentIndex(0)
        elif self.current_step == 1:
            self.subtitle.setText("Product Selection")
            self.desc.setText("Select products to add to this quote")
            self.steps_stack.setCurrentIndex(1)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _go_to_product_selection(self):
        self.current_step = 1
        self._update_step()

    def _go_to_customer_info(self):
        self.current_step = 0
        self._update_step()

    def _open_product_dialog(self):
        dialog = ProductSelectionDialog(self)
        if dialog.exec():
            product_data = dialog.product_added.args[0] if dialog.product_added.args else None
            # For now, just print the result. Later, add to quote items list.
            print("Product added to quote:", product_data) 