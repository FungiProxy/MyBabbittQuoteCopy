"""
User Profile Dialog for the Babbitt Quote Generator.

This dialog displays information about the currently logged-in user.
"""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)


class UserProfileDialog(QDialog):
    """
    A simple dialog to display user profile information.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('User Profile')
        self.setMinimumWidth(300)

        main_layout = QVBoxLayout(self)

        # --- User Info ---
        form_layout = QFormLayout()
        form_layout.addRow('Name:', QLabel('John Smith (Admin)'))
        form_layout.addRow('Email:', QLabel('john.smith@example.com'))
        form_layout.addRow('Role:', QLabel('Administrator'))

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(15)

        # --- Buttons ---
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        main_layout.addWidget(button_box)

        # For V1, this is a static display. Future versions would load
        # this data from a user service or configuration.
