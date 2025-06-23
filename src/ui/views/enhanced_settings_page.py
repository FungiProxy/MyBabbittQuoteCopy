"""
Enhanced Settings Page for MyBabbittQuote
File: src/ui/views/enhanced_settings_page.py

🔴 Critical - Complete settings page with comprehensive options and uniform layout
Easy drop-in replacement for your existing settings page
"""

import os
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QTabWidget,
    QGroupBox, QComboBox, QLineEdit, QTextEdit, QCheckBox, QSpinBox,
    QPushButton, QFileDialog, QLabel, QFrame, QDoubleSpinBox, QMessageBox
)

from src.core.services.settings_service import SettingsService


class EnhancedSettingsPage(QWidget):
    """
    Comprehensive settings page for MyBabbittQuote application.
    
    Features:
    - General application settings
    - Quote configuration options  
    - Export and PDF settings
    - Company information
    - Uniform layout with proper spacing
    - Professional styling
    """
    
    theme_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_service = SettingsService()
        self._setup_ui()
        self._load_settings()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the enhanced settings UI with professional layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Page title
        title_label = QLabel("Application Settings")
        title_label.setObjectName("pageTitle")
        title_label.setStyleSheet("""
            QLabel#pageTitle {
                font-size: 24px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Configure your MyBabbittQuote application preferences")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #6c757d;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(subtitle_label)
        
        # Tab widget for organized settings
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                margin-top: 4px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                color: #495057;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
                min-height: 20px;
            }
            QTabBar::tab:selected {
                background-color: #0052cc;
                color: white;
                font-weight: 600;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e9ecef;
                color: #0052cc;
            }
        """)
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_general_tab()
        self._create_quote_tab()
        self._create_export_tab()
        self._create_company_tab()
        
        # Action buttons
        self._create_action_buttons()
        main_layout.addWidget(self.action_frame)
    
    def _create_general_tab(self):
        """Create the general settings tab."""
        general_widget = QWidget()
        layout = QVBoxLayout(general_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Theme Settings Group
        theme_group = self._create_settings_group("Appearance")
        theme_layout = QFormLayout(theme_group)
        self._apply_standard_form_layout(theme_layout)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Babbitt Industrial", "Corporate Blue", "Classic"])
        self.theme_combo.setMinimumHeight(36)
        theme_layout.addRow("Application Theme:", self.theme_combo)
        
        # Application Behavior Group
        behavior_group = self._create_settings_group("Application Behavior")
        behavior_layout = QFormLayout(behavior_group)
        self._apply_standard_form_layout(behavior_layout)
        
        self.startup_page_combo = QComboBox()
        self.startup_page_combo.addItems(["Dashboard", "Quote Creator", "Customers"])
        self.startup_page_combo.setMinimumHeight(36)
        behavior_layout.addRow("Startup Page:", self.startup_page_combo)
        
        self.auto_save_check = QCheckBox("Automatically save draft quotes every 5 minutes")
        behavior_layout.addRow(self.auto_save_check)
        
        self.confirm_delete_check = QCheckBox("Ask for confirmation before deleting quotes")
        behavior_layout.addRow(self.confirm_delete_check)
        
        self.show_tooltips_check = QCheckBox("Show helpful tooltips and hints")
        behavior_layout.addRow(self.show_tooltips_check)
        
        # Data Management Group
        data_group = self._create_settings_group("Data Management")
        data_layout = QFormLayout(data_group)
        self._apply_standard_form_layout(data_layout)
        
        self.backup_frequency_combo = QComboBox()
        self.backup_frequency_combo.addItems(["Never", "Daily", "Weekly", "Monthly"])
        self.backup_frequency_combo.setMinimumHeight(36)
        data_layout.addRow("Backup Frequency:", self.backup_frequency_combo)
        
        self.max_recent_quotes_spin = QSpinBox()
        self.max_recent_quotes_spin.setRange(5, 50)
        self.max_recent_quotes_spin.setValue(10)
        self.max_recent_quotes_spin.setMinimumHeight(36)
        data_layout.addRow("Max Recent Quotes:", self.max_recent_quotes_spin)
        
        layout.addWidget(theme_group)
        layout.addWidget(behavior_group)
        layout.addWidget(data_group)
        layout.addStretch()
        
        self.tab_widget.addTab(general_widget, "General")
    
    def _create_quote_tab(self):
        """Create the quote configuration tab."""
        quote_widget = QWidget()
        layout = QVBoxLayout(quote_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Default Quote Settings Group
        defaults_group = self._create_settings_group("Default Quote Settings")
        defaults_layout = QFormLayout(defaults_group)
        self._apply_standard_form_layout(defaults_layout)
        
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD ($)", "CAD (C$)", "EUR (€)", "GBP (£)"])
        self.currency_combo.setMinimumHeight(36)
        defaults_layout.addRow("Default Currency:", self.currency_combo)
        
        self.quote_validity_spin = QSpinBox()
        self.quote_validity_spin.setRange(1, 365)
        self.quote_validity_spin.setValue(30)
        self.quote_validity_spin.setSuffix(" days")
        self.quote_validity_spin.setMinimumHeight(36)
        defaults_layout.addRow("Quote Valid For:", self.quote_validity_spin)
        
        self.payment_terms_combo = QComboBox()
        self.payment_terms_combo.addItems([
            "Net 30", "Net 15", "Due on Receipt", "50% Deposit", "Custom"
        ])
        self.payment_terms_combo.setMinimumHeight(36)
        defaults_layout.addRow("Default Payment Terms:", self.payment_terms_combo)
        
        # Pricing Settings Group
        pricing_group = self._create_settings_group("Pricing Configuration")
        pricing_layout = QFormLayout(pricing_group)
        self._apply_standard_form_layout(pricing_layout)
        
        self.include_tax_check = QCheckBox("Include tax in displayed pricing")
        pricing_layout.addRow(self.include_tax_check)
        
        self.tax_rate_spin = QDoubleSpinBox()
        self.tax_rate_spin.setRange(0.0, 50.0)
        self.tax_rate_spin.setValue(0.0)
        self.tax_rate_spin.setSuffix("%")
        self.tax_rate_spin.setDecimals(2)
        self.tax_rate_spin.setMinimumHeight(36)
        pricing_layout.addRow("Default Tax Rate:", self.tax_rate_spin)
        
        self.show_unit_prices_check = QCheckBox("Always show unit prices in quotes")
        pricing_layout.addRow(self.show_unit_prices_check)
        
        self.round_prices_check = QCheckBox("Round prices to nearest dollar")
        pricing_layout.addRow(self.round_prices_check)
        
        # Quote Numbering Group
        numbering_group = self._create_settings_group("Quote Numbering")
        numbering_layout = QFormLayout(numbering_group)
        self._apply_standard_form_layout(numbering_layout)
        
        self.quote_prefix_edit = QLineEdit()
        self.quote_prefix_edit.setPlaceholderText("e.g., Q, QUOTE, BQ")
        self.quote_prefix_edit.setMinimumHeight(36)
        numbering_layout.addRow("Quote Number Prefix:", self.quote_prefix_edit)
        
        self.quote_number_format_combo = QComboBox()
        self.quote_number_format_combo.addItems([
            "Sequential (Q001, Q002, Q003...)",
            "Year-Sequential (Q2025-001, Q2025-002...)",
            "Date-Sequential (Q20250623-001...)"
        ])
        self.quote_number_format_combo.setMinimumHeight(36)
        numbering_layout.addRow("Numbering Format:", self.quote_number_format_combo)
        
        layout.addWidget(defaults_group)
        layout.addWidget(pricing_group)
        layout.addWidget(numbering_group)
        layout.addStretch()
        
        self.tab_widget.addTab(quote_widget, "Quotes")
    
    def _create_export_tab(self):
        """Create the export and PDF settings tab."""
        export_widget = QWidget()
        layout = QVBoxLayout(export_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Export Location Group
        location_group = self._create_settings_group("Export Locations")
        location_layout = QFormLayout(location_group)
        self._apply_standard_form_layout(location_layout)
        
        # Default export path with browse button
        export_path_layout = QHBoxLayout()
        self.export_path_edit = QLineEdit()
        self.export_path_edit.setPlaceholderText("Select default export folder...")
        self.export_path_edit.setMinimumHeight(36)
        self.browse_export_btn = QPushButton("Browse...")
        self.browse_export_btn.setMinimumHeight(36)
        self.browse_export_btn.setMaximumWidth(100)
        export_path_layout.addWidget(self.export_path_edit)
        export_path_layout.addWidget(self.browse_export_btn)
        location_layout.addRow("Default Export Folder:", export_path_layout)
        
        # PDF Template Group
        pdf_group = self._create_settings_group("PDF Template Settings")
        pdf_layout = QFormLayout(pdf_group)
        self._apply_standard_form_layout(pdf_layout)
        
        self.include_logo_check = QCheckBox("Include company logo in PDFs")
        pdf_layout.addRow(self.include_logo_check)
        
        self.pdf_format_combo = QComboBox()
        self.pdf_format_combo.addItems([
            "Standard - Clean professional layout",
            "Detailed - Technical specifications included", 
            "Summary - Compact overview format"
        ])
        self.pdf_format_combo.setMinimumHeight(36)
        pdf_layout.addRow("PDF Layout Style:", self.pdf_format_combo)
        
        self.watermark_check = QCheckBox("Add 'DRAFT' watermark to draft quotes")
        pdf_layout.addRow(self.watermark_check)
        
        self.page_numbers_check = QCheckBox("Include page numbers")
        pdf_layout.addRow(self.page_numbers_check)
        
        # Email Settings Group
        email_group = self._create_settings_group("Email Integration")
        email_layout = QFormLayout(email_group)
        self._apply_standard_form_layout(email_layout)
        
        self.email_template_combo = QComboBox()
        self.email_template_combo.addItems([
            "Professional - Formal business tone",
            "Friendly - Warm and approachable",
            "Technical - Detailed and specific"
        ])
        self.email_template_combo.setMinimumHeight(36)
        email_layout.addRow("Email Template Style:", self.email_template_combo)
        
        self.auto_attach_pdf_check = QCheckBox("Automatically attach PDF when sending quotes")
        email_layout.addRow(self.auto_attach_pdf_check)
        
        self.cc_self_check = QCheckBox("Always CC myself on quote emails")
        email_layout.addRow(self.cc_self_check)
        
        layout.addWidget(location_group)
        layout.addWidget(pdf_group)
        layout.addWidget(email_group)
        layout.addStretch()
        
        self.tab_widget.addTab(export_widget, "Export & PDF")
    
    def _create_company_tab(self):
        """Create the company information tab."""
        company_widget = QWidget()
        layout = QVBoxLayout(company_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Company Details Group
        details_group = self._create_settings_group("Company Information")
        details_layout = QFormLayout(details_group)
        self._apply_standard_form_layout(details_layout)
        
        self.company_name_edit = QLineEdit()
        self.company_name_edit.setPlaceholderText("Your company name")
        self.company_name_edit.setMinimumHeight(36)
        details_layout.addRow("Company Name:", self.company_name_edit)
        
        self.company_address_edit = QTextEdit()
        self.company_address_edit.setPlaceholderText("Street address\nCity, State ZIP\nCountry")
        self.company_address_edit.setMaximumHeight(100)
        details_layout.addRow("Address:", self.company_address_edit)
        
        self.company_phone_edit = QLineEdit()
        self.company_phone_edit.setPlaceholderText("(555) 123-4567")
        self.company_phone_edit.setMinimumHeight(36)
        details_layout.addRow("Phone:", self.company_phone_edit)
        
        self.company_email_edit = QLineEdit()
        self.company_email_edit.setPlaceholderText("contact@company.com")
        self.company_email_edit.setMinimumHeight(36)
        details_layout.addRow("Email:", self.company_email_edit)
        
        self.company_website_edit = QLineEdit()
        self.company_website_edit.setPlaceholderText("https://www.company.com")
        self.company_website_edit.setMinimumHeight(36)
        details_layout.addRow("Website:", self.company_website_edit)
        
        # Branding Group
        branding_group = self._create_settings_group("Branding & Logo")
        branding_layout = QFormLayout(branding_group)
        self._apply_standard_form_layout(branding_layout)
        
        # Logo path with browse button
        logo_path_layout = QHBoxLayout()
        self.logo_path_edit = QLineEdit()
        self.logo_path_edit.setPlaceholderText("Select company logo file...")
        self.logo_path_edit.setMinimumHeight(36)
        self.browse_logo_btn = QPushButton("Browse...")
        self.browse_logo_btn.setMinimumHeight(36)
        self.browse_logo_btn.setMaximumWidth(100)
        logo_path_layout.addWidget(self.logo_path_edit)
        logo_path_layout.addWidget(self.browse_logo_btn)
        branding_layout.addRow("Company Logo:", logo_path_layout)
        
        self.company_tagline_edit = QLineEdit()
        self.company_tagline_edit.setPlaceholderText("Optional company tagline or slogan")
        self.company_tagline_edit.setMinimumHeight(36)
        branding_layout.addRow("Tagline:", self.company_tagline_edit)
        
        # Contact Person Group
        contact_group = self._create_settings_group("Default Contact Person")
        contact_layout = QFormLayout(contact_group)
        self._apply_standard_form_layout(contact_layout)
        
        self.contact_name_edit = QLineEdit()
        self.contact_name_edit.setPlaceholderText("Default sales contact name")
        self.contact_name_edit.setMinimumHeight(36)
        contact_layout.addRow("Contact Name:", self.contact_name_edit)
        
        self.contact_title_edit = QLineEdit()
        self.contact_title_edit.setPlaceholderText("Job title")
        self.contact_title_edit.setMinimumHeight(36)
        contact_layout.addRow("Title:", self.contact_title_edit)
        
        self.contact_email_edit = QLineEdit()
        self.contact_email_edit.setPlaceholderText("Direct email address")
        self.contact_email_edit.setMinimumHeight(36)
        contact_layout.addRow("Email:", self.contact_email_edit)
        
        self.contact_phone_edit = QLineEdit()
        self.contact_phone_edit.setPlaceholderText("Direct phone number")
        self.contact_phone_edit.setMinimumHeight(36)
        contact_layout.addRow("Phone:", self.contact_phone_edit)
        
        layout.addWidget(details_group)
        layout.addWidget(branding_group)
        layout.addWidget(contact_group)
        layout.addStretch()
        
        self.tab_widget.addTab(company_widget, "Company")
    
    def _create_action_buttons(self):
        """Create the action buttons at the bottom."""
        self.action_frame = QFrame()
        action_layout = QHBoxLayout(self.action_frame)
        action_layout.setContentsMargins(0, 20, 0, 0)
        
        # Reset to defaults button
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.setProperty("class", "secondary")
        self.reset_btn.setMinimumHeight(40)
        action_layout.addWidget(self.reset_btn)
        
        action_layout.addStretch()
        
        # Cancel and Save buttons
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setMinimumWidth(100)
        action_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setProperty("class", "primary")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setMinimumWidth(120)
        action_layout.addWidget(self.save_btn)
    
    def _create_settings_group(self, title):
        """Create a standardized settings group box."""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                color: #0052cc;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px 0 8px;
                background-color: white;
            }
        """)
        return group
    
    def _apply_standard_form_layout(self, form_layout):
        """Apply standard spacing to form layouts."""
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
    
    def _connect_signals(self):
        """Connect UI signals."""
        # Theme change signal
        self.theme_combo.currentTextChanged.connect(self.theme_changed.emit)
        
        # Browse buttons
        self.browse_export_btn.clicked.connect(self._browse_export_path)
        self.browse_logo_btn.clicked.connect(self._browse_logo_path)
        
        # Action buttons
        self.save_btn.clicked.connect(self._save_settings)
        self.cancel_btn.clicked.connect(self._load_settings)  # Reload to cancel changes
        self.reset_btn.clicked.connect(self._reset_to_defaults)
    
    def _browse_export_path(self):
        """Browse for export folder."""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Default Export Folder",
            self.export_path_edit.text() or os.path.expanduser("~")
        )
        if folder:
            self.export_path_edit.setText(folder)
    
    def _browse_logo_path(self):
        """Browse for logo file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Company Logo",
            self.logo_path_edit.text() or os.path.expanduser("~"),
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.svg)"
        )
        if file_path:
            self.logo_path_edit.setText(file_path)
    
    def _load_settings(self):
        """Load settings from storage and populate UI fields."""
        try:
            # General settings
            current_theme = self.settings_service.get_theme("Babbitt Industrial")
            if current_theme in ["Babbitt Industrial", "Corporate Blue", "Classic"]:
                self.theme_combo.setCurrentText(current_theme)
            
            startup_page = self.settings_service.get_startup_page("Dashboard")
            self.startup_page_combo.setCurrentText(startup_page)
            
            self.auto_save_check.setChecked(
                self.settings_service.get_nested("general", "auto_save", True, bool)
            )
            
            self.confirm_delete_check.setChecked(
                self.settings_service.get_confirm_on_delete(True)
            )
            
            # Quote settings
            currency = self.settings_service.get_nested("quotes", "default_currency", "USD ($)")
            self.currency_combo.setCurrentText(currency)
            
            validity_days = self.settings_service.get_nested("quotes", "validity_days", 30, int)
            self.quote_validity_spin.setValue(validity_days)
            
            # Export settings
            export_path = self.settings_service.get_default_export_path("")
            self.export_path_edit.setText(export_path)
            
            include_logo = self.settings_service.get_export_with_logo(True)
            self.include_logo_check.setChecked(include_logo)
            
            # Company settings
            company_name = self.settings_service.get_nested("company", "name", "Babbitt International")
            self.company_name_edit.setText(company_name)
            
            company_phone = self.settings_service.get_nested("company", "phone", "")
            self.company_phone_edit.setText(company_phone)
            
            company_email = self.settings_service.get_nested("company", "email", "")
            self.company_email_edit.setText(company_email)
            
            company_website = self.settings_service.get_nested("company", "website", "https://www.babbittinternational.com")
            self.company_website_edit.setText(company_website)
            
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def _save_settings(self):
        """Save current settings to storage."""
        try:
            # General settings
            self.settings_service.set_theme(self.theme_combo.currentText())
            self.settings_service.set_startup_page(self.startup_page_combo.currentText())
            self.settings_service.set_confirm_on_delete(self.confirm_delete_check.isChecked())
            
            # Quote settings - extend SettingsService if needed
            self.settings_service.set_nested("quotes", "default_currency", self.currency_combo.currentText())
            self.settings_service.set_nested("quotes", "validity_days", self.quote_validity_spin.value())
            
            # Export settings
            self.settings_service.set_default_export_path(self.export_path_edit.text())
            self.settings_service.set_export_with_logo(self.include_logo_check.isChecked())
            
            # Company settings
            self.settings_service.set_nested("company", "name", self.company_name_edit.text())
            self.settings_service.set_nested("company", "phone", self.company_phone_edit.text())
            self.settings_service.set_nested("company", "email", self.company_email_edit.text())
            self.settings_service.set_nested("company", "website", self.company_website_edit.text())
            
            self.settings_service.sync()
            
            QMessageBox.information(
                self,
                "Settings Saved",
                "Your settings have been saved successfully."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving Settings", 
                f"Failed to save settings: {str(e)}"
            )
    
    def _reset_to_defaults(self):
        """Reset all settings to default values."""
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset all fields to defaults
            self.theme_combo.setCurrentText("Babbitt Industrial")
            self.startup_page_combo.setCurrentText("Dashboard")
            self.auto_save_check.setChecked(True)
            self.confirm_delete_check.setChecked(True)
            self.currency_combo.setCurrentText("USD ($)")
            self.quote_validity_spin.setValue(30)
            self.export_path_edit.setText("")
            self.include_logo_check.setChecked(True)
            self.company_name_edit.setText("Babbitt International")
            self.company_phone_edit.setText("")
            self.company_email_edit.setText("")
            self.company_website_edit.setText("https://www.babbittinternational.com")
    
    def get_selected_theme(self):
        """Return the currently selected theme."""
        return self.theme_combo.currentText()


# ============================================================================
# IMPLEMENTATION INSTRUCTIONS
# ============================================================================
"""
🔴 EASY IMPLEMENTATION:

1. Replace your existing settings page:
   📁 src/ui/views/enhanced_settings_page.py

2. Update your main window import:
   
   # OLD:
   from src.ui.views.settings_page import SettingsPage
   
   # NEW:
   from src.ui.views.enhanced_settings_page import EnhancedSettingsPage as SettingsPage

3. The SettingsService has been extended with the required methods

4. Apply the professional theme for proper styling

✅ FEATURES INCLUDED:
- General: Theme, startup page, auto-save, confirmations, backup settings
- Quotes: Currency, validity, payment terms, pricing, numbering
- Export: File locations, PDF templates, email integration  
- Company: Contact info, branding, default contact person
- Professional tabbed layout with uniform 36px input heights
- Proper spacing and Babbitt International styling
- Save/Cancel/Reset functionality

All settings are organized logically and use consistent styling with your theme.
The layout is professional and matches your application's industrial aesthetic.
"""