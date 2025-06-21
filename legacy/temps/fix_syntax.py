#!/usr/bin/env python3


def fix_syntax_error():
    """Fix the orphaned except block in product_selection_dialog.py"""

    with open("src/ui/product_selection_dialog.py") as f:
        lines = f.readlines()

    # Find and remove the orphaned except block
    new_lines = []

    for i, line in enumerate(lines):
        if i == 435:  # Line with orphaned except
            continue
        elif i == 436:  # Line with logger.error
            continue
        elif i == 437:  # Line with QMessageBox.critical
            continue
        elif i == 438:  # Line with closing parenthesis
            continue
        elif i == 439:  # Line with closing parenthesis
            continue
        else:
            new_lines.append(line)

    # Write the fixed file
    with open("src/ui/product_selection_dialog.py", "w") as f:
        f.writelines(new_lines)

    print("Fixed syntax error in product_selection_dialog.py")


if __name__ == "__main__":
    fix_syntax_error()
