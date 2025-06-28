#!/usr/bin/env python3
"""
Codebase Cleanup Script
Organizes files into appropriate directories and removes unnecessary files.
"""

import os
import shutil
import glob
from pathlib import Path

def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def move_files_with_pattern(pattern, target_dir, description):
    """Move files matching pattern to target directory."""
    files = glob.glob(pattern)
    if files:
        create_directory_if_not_exists(target_dir)
        for file in files:
            if os.path.isfile(file):
                target_path = os.path.join(target_dir, os.path.basename(file))
                if os.path.exists(target_path):
                    print(f"Warning: {target_path} already exists, skipping {file}")
                    continue
                try:
                    shutil.move(file, target_path)
                    print(f"Moved {file} to {target_dir}")
                except Exception as e:
                    print(f"Error moving {file}: {e}")
        print(f"Moved {len(files)} {description} files to {target_dir}")

def cleanup_root_directory():
    """Clean up files in the root directory."""
    print("\n=== Cleaning Root Directory ===")
    
    # Move debug files
    move_files_with_pattern("debug_*.py", "extra/debug", "debug")
    
    # Move test files (except those in tests/ directory)
    test_files = glob.glob("test_*.py")
    create_directory_if_not_exists("extra/tests")
    for file in test_files:
        if not file.startswith("tests/"):
            target_path = os.path.join("extra/tests", os.path.basename(file))
            if os.path.exists(target_path):
                print(f"Warning: {target_path} already exists, skipping {file}")
                continue
            try:
                shutil.move(file, target_path)
                print(f"Moved {file} to extra/tests/")
            except Exception as e:
                print(f"Error moving {file}: {e}")
    
    # Move check files
    move_files_with_pattern("check_*.py", "extra/checks", "check")
    
    # Move fix files
    move_files_with_pattern("fix_*.py", "extra/fixes", "fix")
    
    # Move database recreation scripts
    move_files_with_pattern("recreate_*.py", "extra/database", "database recreation")
    move_files_with_pattern("restore_*.py", "extra/database", "database restore")
    move_files_with_pattern("rebuild_*.py", "extra/database", "database rebuild")
    move_files_with_pattern("complete_migration.py", "extra/database", "migration")
    move_files_with_pattern("export_db_snapshot.py", "extra/database", "export")
    
    # Move material-related scripts
    move_files_with_pattern("*material*.py", "extra/materials", "material")
    
    # Move simple test files
    move_files_with_pattern("simple_test.py", "extra/tests", "simple test")
    
    # Move configuration files that aren't core
    if os.path.exists("material_options_config.py"):
        create_directory_if_not_exists("extra/config")
        target_path = os.path.join("extra/config", "material_options_config.py")
        if not os.path.exists(target_path):
            try:
                shutil.move("material_options_config.py", target_path)
                print("Moved material_options_config.py to extra/config/")
            except Exception as e:
                print(f"Error moving material_options_config.py: {e}")
    
    # Move review files
    if os.path.exists("review_base_models.py"):
        create_directory_if_not_exists("extra/reviews")
        target_path = os.path.join("extra/reviews", "review_base_models.py")
        if not os.path.exists(target_path):
            try:
                shutil.move("review_base_models.py", target_path)
                print("Moved review_base_models.py to extra/reviews/")
            except Exception as e:
                print(f"Error moving review_base_models.py: {e}")

def cleanup_extra_directory():
    """Organize files within the extra directory."""
    print("\n=== Organizing Extra Directory ===")
    
    # Create subdirectories in extra
    subdirs = [
        "debug", "tests", "checks", "fixes", "database", 
        "materials", "config", "reviews", "analysis", "migration"
    ]
    
    for subdir in subdirs:
        create_directory_if_not_exists(f"extra/{subdir}")
    
    # Move analysis files
    analysis_files = [
        "analyze_*.py", "audit_*.py", "detailed_*.py"
    ]
    for pattern in analysis_files:
        move_files_with_pattern(f"extra/{pattern}", "extra/analysis", "analysis")
    
    # Move migration files
    migration_files = [
        "migrate_*.py", "integrate_*.py"
    ]
    for pattern in migration_files:
        move_files_with_pattern(f"extra/{pattern}", "extra/migration", "migration")
    
    # Move verification files
    verify_files = glob.glob("extra/verify_*.py")
    create_directory_if_not_exists("extra/checks")
    for file in verify_files:
        target_path = os.path.join("extra/checks", os.path.basename(file))
        if not os.path.exists(target_path):
            try:
                shutil.move(file, target_path)
                print(f"Moved {file} to extra/checks/")
            except Exception as e:
                print(f"Error moving {file}: {e}")

def cleanup_legacy_directory():
    """Clean up legacy directory."""
    print("\n=== Cleaning Legacy Directory ===")
    
    # Move backup database files to a backups subdirectory
    backup_files = glob.glob("legacy/quotes_backup_*.db")
    if backup_files:
        create_directory_if_not_exists("legacy/backups")
        for file in backup_files:
            target_path = os.path.join("legacy/backups", os.path.basename(file))
            if not os.path.exists(target_path):
                try:
                    shutil.move(file, target_path)
                    print(f"Moved {file} to legacy/backups/")
                except Exception as e:
                    print(f"Error moving {file}: {e}")
    
    # Move test output files
    output_files = ["legacy/test_*.txt", "legacy/test_*.log"]
    for pattern in output_files:
        files = glob.glob(pattern)
        if files:
            create_directory_if_not_exists("legacy/test_outputs")
            for file in files:
                target_path = os.path.join("legacy/test_outputs", os.path.basename(file))
                if not os.path.exists(target_path):
                    try:
                        shutil.move(file, target_path)
                        print(f"Moved {file} to legacy/test_outputs/")
                    except Exception as e:
                        print(f"Error moving {file}: {e}")

def cleanup_ui_redesign():
    """Organize UI redesign files."""
    print("\n=== Organizing UI Redesign Files ===")
    
    ui_redesign_dir = "data/ui_redesign"
    if os.path.exists(ui_redesign_dir):
        # Move UI files to src/ui/legacy
        create_directory_if_not_exists("src/ui/legacy")
        
        ui_files = [
            "improved_config_ui.py",
            "modern_ui_styles.py", 
            "existing_dialog_fixes.py",
            "ui_integration_guide.py"
        ]
        
        for file in ui_files:
            source = os.path.join(ui_redesign_dir, file)
            if os.path.exists(source):
                target_path = os.path.join("src/ui/legacy", file)
                if not os.path.exists(target_path):
                    try:
                        shutil.move(source, target_path)
                        print(f"Moved {source} to src/ui/legacy/")
                    except Exception as e:
                        print(f"Error moving {source}: {e}")

def remove_duplicate_files():
    """Remove duplicate or unnecessary files."""
    print("\n=== Removing Duplicate Files ===")
    
    # Files that can be safely removed (they have better versions elsewhere)
    files_to_remove = [
        "recreate_database.py",  # Use recreate_database_complete.py instead
        "recreate_full_database.py",  # Use recreate_database_complete.py instead
        "generate_complete_recreation_script.py",  # Functionality integrated into recreate_database_complete.py
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Removed duplicate file: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")

def create_cleanup_summary():
    """Create a summary of the cleanup."""
    print("\n=== Cleanup Summary ===")
    
    summary = """
# Codebase Cleanup Summary

## Files Organized:
- Debug files moved to: extra/debug/
- Test files moved to: extra/tests/
- Check files moved to: extra/checks/
- Fix files moved to: extra/fixes/
- Database scripts moved to: extra/database/
- Material scripts moved to: extra/materials/
- Analysis files moved to: extra/analysis/
- Migration files moved to: extra/migration/
- UI redesign files moved to: src/ui/legacy/

## Directories Created:
- extra/debug/
- extra/tests/
- extra/checks/
- extra/fixes/
- extra/database/
- extra/materials/
- extra/analysis/
- extra/migration/
- extra/config/
- extra/reviews/
- legacy/backups/
- legacy/test_outputs/
- src/ui/legacy/

## Files Removed:
- Duplicate database recreation scripts
- Outdated generation scripts

## Next Steps:
1. Review the organized files in extra/ directory
2. Consider removing files in extra/ that are no longer needed
3. Update any import statements that may be broken
4. Test the application to ensure everything still works
"""
    
    with open("CLEANUP_SUMMARY.md", "w") as f:
        f.write(summary)
    
    print("Created CLEANUP_SUMMARY.md")

def main():
    """Main cleanup function."""
    print("Starting codebase cleanup...")
    
    # Create necessary directories first
    create_directory_if_not_exists("extra")
    create_directory_if_not_exists("legacy")
    
    # Perform cleanup operations
    cleanup_root_directory()
    cleanup_extra_directory()
    cleanup_legacy_directory()
    cleanup_ui_redesign()
    remove_duplicate_files()
    create_cleanup_summary()
    
    print("\n=== Cleanup Complete ===")
    print("Review the CLEANUP_SUMMARY.md file for details.")
    print("Test your application to ensure everything still works correctly.")

if __name__ == "__main__":
    main() 