"""
Settings Service

Manages application settings and preferences.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsService:
    """Service for managing application settings."""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = Path(settings_file)
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_settings()
        return self._get_default_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            "window_size": [1400, 800],
            "window_position": None,
            "theme": "Corporate",
            "recent_files": [],
            "auto_save": True,
            "auto_save_interval": 300,  # 5 minutes
            "default_currency": "USD",
            "company_name": "Babbitt International",
            "company_address": "",
            "company_phone": "",
            "company_email": "",
            "default_quote_validity_days": 30,
            "email_settings": {
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "use_tls": True
            }
        }
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            print(f"Failed to save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
        self._save_settings()
    
    def get_window_size(self) -> list:
        """Get saved window size."""
        return self.settings.get("window_size", [1400, 800])
    
    def set_window_size(self, width: int, height: int):
        """Set window size."""
        self.settings["window_size"] = [width, height]
        self._save_settings()
    
    def get_window_position(self) -> Optional[list]:
        """Get saved window position."""
        return self.settings.get("window_position")
    
    def set_window_position(self, x: int, y: int):
        """Set window position."""
        self.settings["window_position"] = [x, y]
        self._save_settings()
    
    def get_recent_files(self) -> list:
        """Get list of recent files."""
        return self.settings.get("recent_files", [])
    
    def add_recent_file(self, file_path: str):
        """Add a file to recent files list."""
        recent_files = self.get_recent_files()
        if file_path in recent_files:
            recent_files.remove(file_path)
        recent_files.insert(0, file_path)
        # Keep only last 10 files
        recent_files = recent_files[:10]
        self.settings["recent_files"] = recent_files
        self._save_settings()
    
    def get_company_info(self) -> Dict[str, str]:
        """Get company information."""
        return {
            "name": self.settings.get("company_name", "Babbitt International"),
            "address": self.settings.get("company_address", ""),
            "phone": self.settings.get("company_phone", ""),
            "email": self.settings.get("company_email", "")
        }
    
    def set_company_info(self, name: str, address: str = "", phone: str = "", email: str = ""):
        """Set company information."""
        self.settings["company_name"] = name
        self.settings["company_address"] = address
        self.settings["company_phone"] = phone
        self.settings["company_email"] = email
        self._save_settings()
    
    def get_email_settings(self) -> Dict[str, Any]:
        """Get email settings."""
        return self.settings.get("email_settings", {})
    
    def set_email_settings(self, settings: Dict[str, Any]):
        """Set email settings."""
        self.settings["email_settings"] = settings
        self._save_settings()
    
    def get_auto_save_settings(self) -> Dict[str, Any]:
        """Get auto-save settings."""
        return {
            "enabled": self.settings.get("auto_save", True),
            "interval": self.settings.get("auto_save_interval", 300)
        }
    
    def set_auto_save_settings(self, enabled: bool, interval: int = 300):
        """Set auto-save settings."""
        self.settings["auto_save"] = enabled
        self.settings["auto_save_interval"] = interval
        self._save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self._get_default_settings()
        self._save_settings()
    
    def get_theme(self, default: str = "Corporate") -> str:
        """Get the saved application theme."""
        return self.settings.get("theme", default)

    def set_theme(self, theme_name: str):
        """Set the application theme."""
        self.settings["theme"] = theme_name
        self._save_settings()
