import os
import re
from pathlib import Path
from typing import List, Tuple

# Define the new import mappings
IMPORT_MAPPINGS = {
    # Core imports
    r"from models\.": "from src.core.models.",
    r"from services\.": "from src.core.services.",
    r"from pricing\.": "from src.core.pricing.",
    r"from config\.": "from src.core.config.",
    r"from database\.": "from src.core.database.",
    # UI imports
    r"from ui\.": "from src.ui.",
    # API imports
    r"from api\.": "from src.api.",
    # Utils imports
    r"from utils\.": "from src.utils.",
    # Export imports
    r"from export\.": "from src.export.",
}


def find_python_files(start_dir: str) -> List[Path]:
    """Find all Python files in the given directory and its subdirectories."""
    python_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    return python_files


def update_imports(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Update import statements in a file according to the new structure.
    Returns (modified, changes) where modified is a boolean indicating if the file was changed
    and changes is a list of strings describing what was changed.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes = []

        # Update imports according to mappings
        for old_pattern, new_pattern in IMPORT_MAPPINGS.items():
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                changes.append(f"Updated {old_pattern} to {new_pattern}")

        # Only write if changes were made
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, changes

        return False, []

    except Exception as e:
        print(f"Error processing {file_path}: {e!s}")
        return False, [f"Error: {e!s}"]


def main():
    # Directories to process
    directories = ["src", "tests"]

    total_files = 0
    modified_files = 0

    print("Starting import statement updates...")

    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist, skipping...")
            continue

        python_files = find_python_files(directory)
        total_files += len(python_files)

        for file_path in python_files:
            print(f"\nProcessing: {file_path}")
            modified, changes = update_imports(file_path)

            if modified:
                modified_files += 1
                print(f"✓ Modified {file_path}")
                for change in changes:
                    print(f"  - {change}")
            else:
                print(f"✓ No changes needed for {file_path}")

    print("\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files modified: {modified_files}")
    print(f"Files unchanged: {total_files - modified_files}")


if __name__ == "__main__":
    main()
