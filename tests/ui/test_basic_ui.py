"""
Tests for basic UI functionality
"""
import pytest
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

@pytest.fixture
def app():
    """Fixture providing a QApplication instance"""
    app = QApplication([])
    yield app
    app.quit()

def test_basic_window(app):
    """Test that we can create and show a basic window"""
    # Create a simple window
    window = QMainWindow()
    window.setWindowTitle("PySide6 Test")
    window.resize(400, 300)
    
    # Create central widget
    central = QWidget()
    window.setCentralWidget(central)
    
    # Create layout
    layout = QVBoxLayout(central)
    
    # Add a label
    label = QLabel("Test Label")
    label.setStyleSheet("font-size: 16px; color: green;")
    layout.addWidget(label)
    
    # Show window
    window.show()
    
    # Verify window properties
    assert window.windowTitle() == "PySide6 Test"
    assert window.isVisible()
    assert isinstance(window.centralWidget(), QWidget)
    
    # Verify label
    assert label.text() == "Test Label"
    assert label.isVisible()

    # Clean up
    window.close() 