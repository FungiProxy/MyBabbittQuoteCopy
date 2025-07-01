#!/usr/bin/env python3
"""
Script to fix empty else blocks in product_selection_dialog_modern.py
"""

import re

def fix_empty_else_blocks(file_path):
    """Fix empty else blocks by adding pass statements."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match else: followed by optional whitespace and comments, then a newline
    # and then either another else/elif/except/finally or end of function/class
    pattern = r'(else:\s*(?:#[^\n]*)?\s*\n)(?=\s*(?:else|elif|except|finally|def|class|\Z))'
    
    # Replace with else: followed by pass
    fixed_content = re.sub(pattern, r'\1        pass\n', content)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed empty else blocks in {file_path}")

if __name__ == "__main__":
    fix_empty_else_blocks("src/ui/product_selection_dialog_modern.py") 