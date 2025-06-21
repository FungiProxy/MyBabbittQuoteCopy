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
from src.ui.theme.babbitt_theme import BabbittTheme


class ThemePreviewWidget(QFrame):
    """Widget to preview theme colors and styling."""
    
    def __init__(self, theme_name, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        self.setObjectName("themePreview")
        self.setFixedSize(200, 120)
        self.setStyleSheet("""
            QFrame#themePreview {
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                padding: 8px;
            }
            QFrame#themePreview:hover {
                border-color: #2196F3;
                background-color: #F5F5F5;
            }
        """)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the preview UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Theme name
        name_label = QLabel(self.theme_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #333;")
        layout.addWidget(name_label)
        
        # Color preview
        preview_frame = QFrame()
        preview_frame.setObjectName("colorPreview")
        preview_layout = QHBoxLayout(preview_frame)
        preview_layout.setContentsMargins(5, 5, 5, 5)
        preview_layout.setSpacing(3)
        
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
        self.settings_service = SettingsService()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # --- General Settings ---
        general_group = QGroupBox("General")
        general_layout = QFormLayout(general_group)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(ThemeManager.get_available_themes())
        general_layout.addRow("Application Theme:", self.theme_combo)

        main_layout.addWidget(general_group)

        # --- Other settings groups would go here ---

        main_layout.addStretch()

        # --- Save Button ---
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setObjectName("saveSettingsButton")
        main_layout.addWidget(self.save_btn, 0, Qt.AlignmentFlag.AlignRight)

        self.load_settings()
        self._connect_signals()

    def _connect_signals(self):
        self.save_btn.clicked.connect(self.save_settings)
        # When the theme combo changes, immediately emit the signal
        self.theme_combo.currentTextChanged.connect(self.theme_changed.emit)

    def load_settings(self):
        """Load settings from storage and populate the UI fields."""
        saved_theme = self.settings_service.get_theme(BabbittTheme.CORPORATE_THEME)
        if saved_theme in ThemeManager.get_available_themes():
            self.theme_combo.setCurrentText(saved_theme)

    def save_settings(self):
        """Save the current settings from the UI to storage."""
        selected_theme = self.theme_combo.currentText()
        self.settings_service.set_theme(selected_theme)
        
        # Also apply the theme immediately upon saving
        self.theme_changed.emit(selected_theme)

        QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully.")
        
    def get_selected_theme(self) -> str:
        """Returns the currently selected theme from the dropdown."""
        return self.theme_combo.currentText()
