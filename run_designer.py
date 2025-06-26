#!/usr/bin/env python3
"""
Simple script to launch Qt Designer
"""
import os
import subprocess
import sys

def main():
    # Path to the designer executable in PySide6 (correct path)
    designer_path = os.path.join(
        os.path.dirname(sys.executable), 
        "Lib", "site-packages", "PySide6", "designer.exe"
    )
    
    # Alternative path that we know exists
    alt_designer_path = r"C:\Users\mchew\OneDrive\Desktop\MyBabbittQuoteCopy\myenv\Lib\site-packages\PySide6\designer.exe"
    
    if os.path.exists(designer_path):
        print(f"Launching Qt Designer from: {designer_path}")
        subprocess.Popen([designer_path])
        print("Qt Designer launched successfully!")
    elif os.path.exists(alt_designer_path):
        print(f"Launching Qt Designer from: {alt_designer_path}")
        subprocess.Popen([alt_designer_path])
        print("Qt Designer launched successfully!")
    else:
        print(f"Qt Designer not found at: {designer_path}")
        print(f"Also not found at: {alt_designer_path}")
        print("Please check your PySide6 installation.")

if __name__ == "__main__":
    main() 