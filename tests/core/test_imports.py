"""
Tests for verifying required imports are available
"""
import pytest

@pytest.mark.parametrize("module_name", [
    "os",
    "sys",
    "traceback",
    "PySide6.QtWidgets",
    "PySide6.QtCore",
    "PySide6.QtGui",
])
def test_base_imports(module_name):
    """Test that base Python and PySide6 modules can be imported"""
    __import__(module_name)

@pytest.mark.parametrize("module_name", [
    "src.ui",
    "src.ui.main_window",
    "src.ui.product_tab",
    "src.ui.specifications_tab",
    "src.ui.quote_tab",
])
def test_application_imports(module_name):
    """Test that application modules can be imported"""
    __import__(module_name) 