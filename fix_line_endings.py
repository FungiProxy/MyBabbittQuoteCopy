import os

def convert_to_lf(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    # Replace CRLF and CR with LF
    new_content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    if content != new_content:
        with open(filepath, 'wb') as f:
            f.write(new_content)
        print(f"Converted: {filepath}")
    else:
        print(f"Already LF: {filepath}")

def process_dir(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                convert_to_lf(os.path.join(dirpath, filename))

if __name__ == "__main__":
    process_dir(".")
    print("All .py files have been converted to LF line endings.")
