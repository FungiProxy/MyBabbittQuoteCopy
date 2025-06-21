"""
Apply Configuration Dialog Fixes
Script to apply the ConfigurationDialogHelper fixes to all existing dialogs.

Run this script to automatically apply the fixes to your configuration dialogs.
"""

import os
import re
from pathlib import Path

def apply_fixes_to_file(file_path: str):
    """Apply configuration dialog fixes to a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if file contains dialog classes
        if not re.search(r'class.*Dialog.*QDialog', content):
            return False, "No dialog classes found"
        
        # Check if ConfigurationDialogHelper is already imported
        if 'ConfigurationDialogHelper' in content:
            return False, "ConfigurationDialogHelper already imported"
        
        # Add import statement
        import_pattern = r'from src\.ui\.components\.configuration_dialog_helper import ConfigurationDialogHelper'
        if import_pattern not in content:
            # Find the last import statement
            import_match = re.search(r'^from.*import.*$', content, re.MULTILINE)
            if import_match:
                # Add import after the last import
                last_import_end = import_match.end()
                content = content[:last_import_end] + '\nfrom src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper\n' + content[last_import_end:]
            else:
                # Add at the beginning after docstring
                docstring_end = content.find('"""', content.find('"""') + 3) + 3
                if docstring_end > 3:
                    content = content[:docstring_end] + '\nfrom src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper\n' + content[docstring_end:]
                else:
                    # Add after first line
                    first_line_end = content.find('\n') + 1
                    content = content[:first_line_end] + 'from src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper\n' + content[first_line_end:]
        
        # Find __init__ methods in dialog classes
        init_pattern = r'def __init__\(self[^)]*\):'
        init_matches = list(re.finditer(init_pattern, content))
        
        if not init_matches:
            return False, "No __init__ methods found"
        
        # Apply fixes to each __init__ method
        for match in reversed(init_matches):  # Process in reverse to maintain positions
            init_start = match.start()
            
            # Find the end of the __init__ method
            lines = content[init_start:].split('\n')
            indent_level = None
            method_end = init_start
            
            for i, line in enumerate(lines):
                if i == 0:  # First line (def __init__)
                    continue
                
                # Find the base indent level
                if indent_level is None and line.strip():
                    indent_level = len(line) - len(line.lstrip())
                    continue
                
                # Check if we've reached the end of the method
                if line.strip() and (len(line) - len(line.lstrip())) <= indent_level:
                    method_end = init_start + len('\n'.join(lines[:i]))
                    break
            
            # Check if ConfigurationDialogHelper.apply_dialog_fixes is already called
            method_content = content[init_start:method_end]
            if 'ConfigurationDialogHelper.apply_dialog_fixes(self)' in method_content:
                continue
            
            # Find a good place to add the fix (after setup_ui or similar)
            setup_ui_pattern = r'\._setup_ui\(\)'
            setup_match = re.search(setup_ui_pattern, method_content)
            
            if setup_match:
                # Add after setup_ui call
                insert_pos = init_start + setup_match.end()
                # Find the end of the line
                line_end = method_content[setup_match.end():].find('\n')
                if line_end != -1:
                    insert_pos += line_end + 1
                
                # Add the fix with proper indentation
                indent = ' ' * (indent_level + 8)  # 8 spaces for method body
                fix_code = f'\n{indent}# Apply configuration dialog fixes\n{indent}ConfigurationDialogHelper.apply_dialog_fixes(self)\n'
                content = content[:insert_pos] + fix_code + content[insert_pos:]
            else:
                # Add at the end of the method
                indent = ' ' * (indent_level + 8)
                fix_code = f'\n{indent}# Apply configuration dialog fixes\n{indent}ConfigurationDialogHelper.apply_dialog_fixes(self)\n'
                content = content[:method_end] + fix_code + content[method_end:]
        
        # Write the modified content back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Fixes applied successfully"
        else:
            return False, "No changes needed"
            
    except Exception as e:
        return False, f"Error processing file: {str(e)}"

def find_dialog_files():
    """Find all Python files that might contain dialog classes."""
    dialog_files = []
    
    # Common directories to search
    search_dirs = [
        'src/ui',
        'src/ui/components',
        'src/ui/dialogs',
        'data/ui_redesign'
    ]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        file_path = os.path.join(root, file)
                        dialog_files.append(file_path)
    
    return dialog_files

def main():
    """Main function to apply fixes to all dialog files."""
    print("🔧 Applying Configuration Dialog Fixes")
    print("=" * 50)
    
    # Find all dialog files
    dialog_files = find_dialog_files()
    
    if not dialog_files:
        print("❌ No dialog files found")
        return
    
    print(f"📁 Found {len(dialog_files)} potential dialog files")
    print()
    
    # Apply fixes to each file
    success_count = 0
    for file_path in dialog_files:
        print(f"🔍 Processing: {file_path}")
        success, message = apply_fixes_to_file(file_path)
        
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"ℹ️  {message}")
        print()
    
    print("=" * 50)
    print(f"🎉 Completed! Applied fixes to {success_count} files")
    print()
    print("📋 Summary of fixes applied:")
    print("   • Added ConfigurationDialogHelper import")
    print("   • Added ConfigurationDialogHelper.apply_dialog_fixes(self) calls")
    print("   • Fixed oversized dropdowns")
    print("   • Improved spacing and layout")
    print("   • Applied consistent section styling")
    print("   • Fixed button styling")
    print("   • Applied modern form styling")

if __name__ == "__main__":
    main() 