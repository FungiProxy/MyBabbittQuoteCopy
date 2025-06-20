"""
Service for managing application settings.

This module provides a service layer for managing application-wide settings,
persisting them using QSettings for platform-independent storage.
"""

from PySide6.QtCore import QSettings


class SettingsService:
    """
    Service class for managing application settings.

    Provides methods for getting and setting application configuration values.
    """

    def __init__(self, company='BabbittInternational', app='QuoteGenerator'):
        self.settings = QSettings(company, app)

    def get_theme(self, default='Default Light'):
        """Retrieves the application theme."""
        return self.settings.value('theme', defaultValue=default)

    def set_theme(self, theme: str):
        """Saves the application theme."""
        self.settings.setValue('theme', theme)

    def get_default_export_path(self, default=''):
        """Retrieves the default path for quote exports."""
        return self.settings.value('export/default_path', defaultValue=default)

    def set_default_export_path(self, path: str):
        """Saves the default path for quote exports."""
        self.settings.setValue('export/default_path', path)

    def get_startup_page(self, default='Dashboard'):
        """Retrieves the default page to show on startup."""
        return self.settings.value('ui/startup_page', defaultValue=default)

    def set_startup_page(self, page_name: str):
        """Saves the default startup page."""
        self.settings.setValue('ui/startup_page', page_name)

    def get_export_with_logo(self, default=True):
        """Checks if the company logo should be included in exports."""
        return self.settings.value('export/with_logo', defaultValue=default, type=bool)

    def set_export_with_logo(self, with_logo: bool):
        """Saves the setting for including the company logo in exports."""
        self.settings.setValue('export/with_logo', with_logo)

    def get_confirm_on_delete(self, default=True):
        """Checks if a confirmation is required before deleting items."""
        return self.settings.value(
            'ui/confirm_on_delete', defaultValue=default, type=bool
        )

    def set_confirm_on_delete(self, confirm: bool):
        """Saves the setting for requiring deletion confirmation."""
        self.settings.setValue('ui/confirm_on_delete', confirm)

    def sync(self):
        """Ensures that any cached writes are written to permanent storage."""
        self.settings.sync()
