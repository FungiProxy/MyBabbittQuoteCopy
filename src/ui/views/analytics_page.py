"""
Placeholder for the Analytics Page.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AnalyticsPage(QWidget):
    """
    A placeholder widget for the Analytics page.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Analytics & Reporting Features Coming Soon!")
        label.setObjectName("placeholderLabel")
        label.setStyleSheet("font-size: 24px; color: #888;")

        layout.addWidget(label)
