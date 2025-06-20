"""
Settings Page for the Babbitt Quote Generator.

This page provides options for configuring the application, such as
setting default paths, managing themes, and other user preferences.
"""

import os
import subprocess
import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGridLayout,
)

from src.core.services.settings_service import SettingsService
from src.ui.theme.theme_manager import ThemeManager


class ThemePreviewWidget(QFrame):
    """Widget for displaying theme previews."""
    
    def __init__(self, theme_info, parent=None):
        super().__init__(parent)
        self.theme_info = theme_info
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the preview UI."""
        self.setFixedSize(120, 80)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme_info['background_color']};
                border: 2px solid #E5E7EB;
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Theme name
        name_label = QLabel(self.theme_info['name'])
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme_info['primary_color']};
                font-weight: 600;
                font-size: 10px;
            }}
        """)
        layout.addWidget(name_label)
        
        # Color preview
        color_frame = QFrame()
        color_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme_info['primary_color']};
                border-radius: 4px;
                min-height: 20px;
            }}
        """)
        layout.addWidget(color_frame)
        
        # Accent color
        accent_frame = QFrame()
        accent_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme_info['accent_color']};
                border-radius: 4px;
                min-height: 8px;
            }}
        """)
        layout.addWidget(accent_frame)


class SettingsPage(QWidget):
    """
    A widget that contains all the settings for the application.
    """

    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.settings_service = SettingsService()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- General Settings ---
        general_group = QGroupBox('General')
        general_layout = QFormLayout(general_group)
        general_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Theme selection with preview
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(ThemeManager.get_available_themes())
        self.theme_combo.setEnabled(True)  # Enable theme selection
        
        # Create theme preview section
        theme_preview_layout = QVBoxLayout()
        theme_preview_layout.addWidget(self.theme_combo)
        
        # Theme previews
        preview_frame = QFrame()
        preview_layout = QGridLayout(preview_frame)
        preview_layout.setSpacing(10)
        
        self.preview_widgets = {}
        for i, theme_name in enumerate(ThemeManager.get_available_themes()):
            theme_info = ThemeManager.get_theme_preview_info(theme_name)
            if theme_info:
                preview_widget = ThemePreviewWidget(theme_info)
                self.preview_widgets[theme_name] = preview_widget
                preview_layout.addWidget(preview_widget, i // 2, i % 2)
        
        theme_preview_layout.addWidget(preview_frame)
        general_layout.addRow('Application Theme:', theme_preview_layout)

        self.startup_page_combo = QComboBox()
        self.startup_page_combo.addItems(['Dashboard', 'Quote Creation', 'Customers'])
        general_layout.addRow('Startup Page:', self.startup_page_combo)

        self.confirm_on_delete_check = QCheckBox('Confirm before deleting quotes')
        general_layout.addRow(self.confirm_on_delete_check)

        main_layout.addWidget(general_group)

        # --- Export Settings ---
        export_group = QGroupBox('Export Settings')
        export_layout = QFormLayout(export_group)

        self.default_export_path_input = QLineEdit()
        self.browse_export_path_btn = QPushButton('Browse...')
        export_path_layout = QHBoxLayout()
        export_path_layout.addWidget(self.default_export_path_input)
        export_path_layout.addWidget(self.browse_export_path_btn)
        export_layout.addRow('Default Export Path:', export_path_layout)

        self.export_with_logo_check = QCheckBox('Include company logo in PDF exports')
        export_layout.addRow(self.export_with_logo_check)

        main_layout.addWidget(export_group)

        # --- Database Settings ---
        db_group = QGroupBox('Database')
        db_layout = QFormLayout(db_group)

        self.db_path_label = QLabel('data/babbitt.db')  # Placeholder
        db_layout.addRow('Database Path:', self.db_path_label)

        self.reseed_btn = QPushButton('Reseed Database')
        db_layout.addWidget(self.reseed_btn)

        main_layout.addWidget(db_group)

        main_layout.addStretch()

        # --- Save/Cancel Buttons ---
        button_layout = QVBoxLayout()
        self.save_btn = QPushButton('Save Settings')
        self.save_btn.setObjectName('saveSettingsButton')
        button_layout.addWidget(self.save_btn)

        main_layout.addLayout(button_layout)

        self.load_settings()
        self._connect_signals()

    def _connect_signals(self):
        self.save_btn.clicked.connect(self.save_settings)
        self.browse_export_path_btn.clicked.connect(self.browse_for_export_path)
        self.reseed_btn.clicked.connect(self.reseed_database)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)

    def _on_theme_changed(self, theme_name):
        """Handle theme selection change."""
        # Emit signal for theme change
        self.theme_changed.emit(theme_name)
        
        # Update preview selection
        self._update_preview_selection(theme_name)

    def _update_preview_selection(self, selected_theme):
        """Update the visual selection of theme previews."""
        for theme_name, preview_widget in self.preview_widgets.items():
            if theme_name == selected_theme:
                preview_widget.setStyleSheet(f"""
                    QFrame {{
                        background-color: {preview_widget.theme_info['background_color']};
                        border: 3px solid #3B82F6;
                        border-radius: 8px;
                    }}
                """)
            else:
                preview_widget.setStyleSheet(f"""
                    QFrame {{
                        background-color: {preview_widget.theme_info['background_color']};
                        border: 2px solid #E5E7EB;
                        border-radius: 8px;
                    }}
                """)

    def load_settings(self):
        """Load settings from storage and populate the UI fields."""
        # Load current theme
        current_theme = self.settings_service.get_theme('Babbitt Theme')
        if current_theme in ThemeManager.get_available_themes():
            self.theme_combo.setCurrentText(current_theme)
        else:
            # Fallback to Babbitt theme if saved theme is not available
            self.theme_combo.setCurrentText('Babbitt Theme')
        
        self._update_preview_selection(self.theme_combo.currentText())

        startup_page = self.settings_service.get_startup_page()
        self.startup_page_combo.setCurrentText(startup_page)

        self.confirm_on_delete_check.setChecked(
            self.settings_service.get_confirm_on_delete()
        )

        export_path = self.settings_service.get_default_export_path(
            os.path.expanduser('~')
        )
        self.default_export_path_input.setText(export_path)

        self.export_with_logo_check.setChecked(
            self.settings_service.get_export_with_logo()
        )

    def save_settings(self):
        """Save the current settings from the UI to storage."""
        # Save selected theme
        selected_theme = self.theme_combo.currentText()
        self.settings_service.set_theme(selected_theme)
        
        self.settings_service.set_startup_page(self.startup_page_combo.currentText())
        self.settings_service.set_confirm_on_delete(
            self.confirm_on_delete_check.isChecked()
        )

        self.settings_service.set_default_export_path(
            self.default_export_path_input.text()
        )
        self.settings_service.set_export_with_logo(
            self.export_with_logo_check.isChecked()
        )

        self.settings_service.sync()

        QMessageBox.information(
            self, 'Settings Saved', 'Your settings have been saved successfully.'
        )

    def browse_for_export_path(self):
        """Open a dialog to select a default export directory."""
        current_path = self.default_export_path_input.text()
        directory = QFileDialog.getExistingDirectory(
            self, 'Select Default Export Path', current_path
        )
        if directory:
            self.default_export_path_input.setText(directory)

    def reseed_database(self):
        """Reseed the database with initial data."""
        reply = QMessageBox.question(
            self,
            'Confirm Database Reseed',
            'This will reset the database to its initial state. All current data will be lost. Continue?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Import and run reseed script
                from scripts.data.init.init_sample_data import init_sample_data
                init_sample_data()
                QMessageBox.information(
                    self, 'Success', 'Database has been reseeded successfully.'
                )
            except Exception as e:
                QMessageBox.critical(
                    self, 'Error', f'Failed to reseed database: {str(e)}'
                )
