"""
Test V0 Integration - Quick Demo

This demonstrates how to integrate your v0ui components with minimal changes
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class ModernSidebar(QWidget):
    """Modern sidebar from v0ui"""
    page_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #0f172a; border-bottom: 1px solid #334155;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        
        logo_label = QLabel("Babbitt")
        logo_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #3b82f6;")
        header_layout.addWidget(logo_label)
        
        layout.addWidget(header)
        
        # Navigation buttons
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(16, 24, 16, 24)
        nav_layout.setSpacing(8)
        
        quote_btn = QPushButton("📝 Quote Creator")
        quote_btn.setMinimumHeight(48)
        quote_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                text-align: left;
            }
        """)
        nav_layout.addWidget(quote_btn)
        
        quotes_btn = QPushButton("📂 All Quotes")
        quotes_btn.setMinimumHeight(48)
        quotes_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #334155;
                color: white;
            }
        """)
        nav_layout.addWidget(quotes_btn)
        
        nav_layout.addStretch()
        layout.addWidget(nav_widget)


class ModernMainWindow(QMainWindow):
    """Modern main window combining v0ui with existing logic"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyBabbittQuote V0 - Babbitt International")
        self.setMinimumSize(1400, 900)
        
        self.setStyleSheet("QMainWindow { background-color: #f8fafc; }")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Modern sidebar
        sidebar = ModernSidebar()
        main_layout.addWidget(sidebar)
        
        # Content area
        content_frame = QWidget()
        content_frame.setStyleSheet("background-color: #f8fafc;")
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(32, 32, 32, 32)
        
        # Modern header
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 24)
        
        title_label = QLabel("Quote Creator")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1e293b;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        new_product_btn = QPushButton("+ New Product")
        new_product_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        header_layout.addWidget(new_product_btn)
        
        content_layout.addWidget(header)
        
        # Main content
        main_content = QWidget()
        main_content.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        main_content_layout = QVBoxLayout(main_content)
        main_content_layout.setContentsMargins(32, 32, 32, 32)
        
        content_label = QLabel("Modern V0 UI successfully integrated!")
        content_label.setFont(QFont("Segoe UI", 16))
        content_label.setStyleSheet("color: #374151; padding: 40px;")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_content_layout.addWidget(content_label)
        
        content_layout.addWidget(main_content)
        
        main_layout.addWidget(content_frame, 1)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = ModernMainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 