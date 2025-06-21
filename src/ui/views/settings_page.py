"""
Settings Page for the Babbitt Quote Generator.

This page provides options for configuring the application, such as
setting default paths, managing themes, and other user preferences.
"""

import os
import subprocess
import sys

from PySide6.QtCore import Qt, Signal
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
from src.ui.helpers.window_layout_helper import fix_configuration_dialog_layout


class ThemePreviewWidget(QFrame):
    """Widget to preview theme colors and styling."""
    
    def __init__(self, theme_name, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the preview widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Theme name
        name_label = QLabel(self.theme_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: 600; font-size: 12px;")
        layout.addWidget(name_label)
        
        # Color preview frame
        preview_frame = QFrame()
        preview_frame.setFixedHeight(40)
        preview_frame.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")
        
        preview_layout = QHBoxLayout(preview_frame)
        preview_layout.setContentsMargins(8, 8, 8, 8)
        preview_layout.setSpacing(8)
        
        # Get theme info
        theme_info = ThemeManager.get_theme_preview_info(self.theme_name)
        if theme_info:
            # Primary color
            primary_color = QFrame()
            primary_color.setFixedSize(30, 30)
            primary_color.setStyleSheet(f"background-color: {theme_info['primary_color']}; border-radius: 15px; border: 1px solid #ccc;")
            preview_layout.addWidget(primary_color)
            
            # Accent color
            accent_color = QFrame()
            accent_color.setFixedSize(30, 30)
            accent_color.setStyleSheet(f"background-color: {theme_info['accent_color']}; border-radius: 15px; border: 1px solid #ccc;")
            preview_layout.addWidget(accent_color)
            
            # Background color
            bg_color = QFrame()
            bg_color.setFixedSize(30, 30)
            bg_color.setStyleSheet(f"background-color: {theme_info['background_color']}; border-radius: 15px; border: 1px solid #ccc;")
            preview_layout.addWidget(bg_color)
        
        layout.addWidget(preview_frame)
        
        # Description
        if theme_info and theme_info.get('description'):
            desc_label = QLabel(theme_info['description'])
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("font-size: 10px; color: #666;")
            layout.addWidget(desc_label)


class SettingsPage(QWidget):
    """
    A widget that contains all the settings for the application.
    """

    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Fix configuration dialog layout
        fix_configuration_dialog_layout(self)
        
        self.setWindowTitle("Settings")
        self.settings_service = SettingsService()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- General Settings ---
        general_group = QGroupBox("General")
        general_layout = QFormLayout(general_group)
        general_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Theme selection with all available themes
        self.theme_combo = QComboBox()
        available_themes = ThemeManager.get_available_themes()
        self.theme_combo.addItems(available_themes)
        general_layout.addRow("Application Theme:", self.theme_combo)

        self.startup_page_combo = QComboBox()
        self.startup_page_combo.addItems(["Dashboard", "Quote Creation", "Customers"])
        general_layout.addRow("Startup Page:", self.startup_page_combo)

        self.confirm_on_delete_check = QCheckBox("Confirm before deleting quotes")
        general_layout.addRow(self.confirm_on_delete_check)

        main_layout.addWidget(general_group)

        # --- Theme Preview ---
        theme_preview_group = QGroupBox("Theme Preview")
        theme_preview_layout = QVBoxLayout(theme_preview_group)
        
        # Theme preview grid
        self.theme_preview_widget = QWidget()
        self.theme_preview_layout = QGridLayout(self.theme_preview_widget)
        self.theme_preview_layout.setSpacing(10)
        
        # Create preview widgets for each theme
        self.preview_widgets = {}
        available_themes = ThemeManager.get_available_themes()
        cols = 3  # Number of columns in the grid
        for i, theme_name in enumerate(available_themes):
            row = i // cols
            col = i % cols
            preview_widget = ThemePreviewWidget(theme_name)
            self.preview_widgets[theme_name] = preview_widget
            self.theme_preview_layout.addWidget(preview_widget, row, col)
        
        theme_preview_layout.addWidget(self.theme_preview_widget)
        main_layout.addWidget(theme_preview_group)

        # --- Export Settings ---
        export_group = QGroupBox("Export Settings")
        export_layout = QFormLayout(export_group)

        self.default_export_path_input = QLineEdit()
        self.browse_export_path_btn = QPushButton("Browse...")
        export_path_layout = QHBoxLayout()
        export_path_layout.addWidget(self.default_export_path_input)
        export_path_layout.addWidget(self.browse_export_path_btn)
        export_layout.addRow("Default Export Path:", export_path_layout)

        self.export_with_logo_check = QCheckBox("Include company logo in PDF exports")
        export_layout.addRow(self.export_with_logo_check)

        main_layout.addWidget(export_group)

        # --- Database Settings ---
        db_group = QGroupBox("Database")
        db_layout = QFormLayout(db_group)

        self.db_path_label = QLabel("data/babbitt.db")  # Placeholder
        db_layout.addRow("Database Path:", self.db_path_label)

        self.reseed_btn = QPushButton("Reseed Database")
        db_layout.addWidget(self.reseed_btn)

        main_layout.addWidget(db_group)

        main_layout.addStretch()

        # --- Save/Cancel Buttons ---
        button_layout = QVBoxLayout()
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setObjectName("saveSettingsButton")
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
        """Handle theme selection change and emit signal."""
        self.theme_changed.emit(theme_name)

    def load_settings(self):
        """Load settings from storage and populate the UI fields."""
        # Load current theme
        current_theme = self.settings_service.get_theme('Modern Babbitt')  # Default to Modern Babbitt
        if current_theme in ThemeManager.get_available_themes():
            self.theme_combo.setCurrentText(current_theme)
        else:
            # If saved theme is not available, default to first available theme
            available_themes = ThemeManager.get_available_themes()
            if available_themes:
                self.theme_combo.setCurrentText(available_themes[0])

        startup_page = self.settings_service.get_startup_page()
        self.startup_page_combo.setCurrentText(startup_page)

        self.confirm_on_delete_check.setChecked(
            self.settings_service.get_confirm_on_delete()
        )

        export_path = self.settings_service.get_default_export_path(
            os.path.expanduser("~")
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
            self, "Settings Saved", "Your settings have been saved successfully."
        )

    def browse_for_export_path(self):
        """Open a dialog to select a default export directory."""
        current_path = self.default_export_path_input.text()
        directory = QFileDialog.getExistingDirectory(
            self, "Select Default Export Path", current_path
        )
        if directory:
            self.default_export_path_input.setText(directory)

    def reseed_database(self):
        """Triggers the database seeding script."""
        reply = QMessageBox.question(
            self,
            "Reseed Database",
            "This will delete all existing data and re-seed the database with default values. Are you sure you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                # Assuming the script is in a 'scripts' folder at the project root
                script_path = os.path.join(os.getcwd(), "scripts", "seed_database.py")
                if not os.path.exists(script_path):
                    QMessageBox.critical(
                        self, "Error", f"Seeding script not found at {script_path}"
                    )
                    return

                # Use the same python executable that is running the app
                python_executable = sys.executable
                subprocess.run(
                    [python_executable, script_path],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                QMessageBox.information(
                    self, "Success", "Database has been re-seeded successfully."
                )
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to re-seed database:\n{e.stderr}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"An unexpected error occurred: {e}"
                )
