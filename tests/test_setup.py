import os
import sys
import traceback

REQUIRED_PACKAGES = [
    ("reportlab", "reportlab.pdfgen.canvas"),
    ("python-docx", "docx"),
    ("Pillow", "PIL.Image"),
]

TEMPLATE_DIR = os.path.join("data", "templates")
REQUIRED_FILES = [
    "pdf_styles.py",
    "email_template.html",
    "README.md",
    "quote_template.docx",
    "pdf_template.py",
]
LOGO_PATH = os.path.join(TEMPLATE_DIR, "logo.png")

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def print_success(msg):
    print(f"\033[92m[SUCCESS]\033[0m {msg}")


def print_failure(msg):
    print(f"\033[91m[FAILURE]\033[0m {msg}")


def print_warning(msg):
    print(f"\033[93m[WARNING]\033[0m {msg}")


def print_info(msg):
    print(f"[INFO] {msg}")


def test_imports():
    print_info("Testing required package imports...")
    for pkg, mod in REQUIRED_PACKAGES:
        try:
            __import__(mod)
            print_success(f"Imported {pkg} ({mod})")
        except Exception as e:
            print_failure(f"Could not import {pkg} ({mod}): {e}")
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)


def test_template_dir():
    print_info(f"Checking template directory: {TEMPLATE_DIR}")
    if not os.path.isdir(TEMPLATE_DIR):
        print_failure(f"Template directory not found: {TEMPLATE_DIR}")
        sys.exit(EXIT_FAILURE)
    print_success(f"Template directory exists: {TEMPLATE_DIR}")


def test_required_files():
    print_info("Checking for required template files...")
    all_ok = True
    for fname in REQUIRED_FILES:
        fpath = os.path.join(TEMPLATE_DIR, fname)
        if not os.path.isfile(fpath):
            print_failure(f"Missing required file: {fpath}")
            all_ok = False
        else:
            if os.path.getsize(fpath) == 0:
                print_warning(f"File exists but is empty: {fpath}")
            else:
                print_success(f"Found required file: {fpath}")
    if not all_ok:
        sys.exit(EXIT_FAILURE)


def test_logo():
    if os.path.isfile(LOGO_PATH):
        print_success(f"Logo file found: {LOGO_PATH}")
    else:
        print_warning(
            f"Logo file not found: {LOGO_PATH} (not fatal, but PDF branding may be incomplete)"
        )


def test_reportlab():
    print_info("Testing basic ReportLab PDF generation...")
    try:
        from reportlab.pdfgen import canvas

        test_pdf = os.path.join(TEMPLATE_DIR, "test_reportlab_output.pdf")
        c = canvas.Canvas(test_pdf)
        c.drawString(100, 750, "ReportLab PDF test successful!")
        c.save()
        if os.path.isfile(test_pdf):
            print_success("ReportLab PDF generated successfully.")
            os.remove(test_pdf)
        else:
            print_failure("ReportLab did not create the PDF file.")
            sys.exit(EXIT_FAILURE)
    except Exception as e:
        print_failure(f"ReportLab PDF generation failed: {e}")
        traceback.print_exc()
        sys.exit(EXIT_FAILURE)


def test_python_docx():
    print_info("Testing basic python-docx functionality...")
    try:
        import docx

        test_docx = os.path.join(TEMPLATE_DIR, "test_docx_output.docx")
        doc = docx.Document()
        doc.add_heading("python-docx test successful!", 0)
        doc.save(test_docx)
        if os.path.isfile(test_docx):
            print_success("python-docx document created successfully.")
            os.remove(test_docx)
        else:
            print_failure("python-docx did not create the DOCX file.")
            sys.exit(EXIT_FAILURE)
    except Exception as e:
        print_failure(f"python-docx test failed: {e}")
        traceback.print_exc()
        sys.exit(EXIT_FAILURE)


def test_pillow():
    print_info("Testing basic Pillow image creation...")
    try:
        from PIL import Image, ImageDraw

        test_img = os.path.join(TEMPLATE_DIR, "test_pillow_output.png")
        img = Image.new("RGB", (200, 100), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 40), "Pillow test!", fill=(255, 255, 0))
        img.save(test_img)
        if os.path.isfile(test_img):
            print_success("Pillow image created successfully.")
            os.remove(test_img)
        else:
            print_failure("Pillow did not create the image file.")
            sys.exit(EXIT_FAILURE)
    except Exception as e:
        print_failure(f"Pillow test failed: {e}")
        traceback.print_exc()
        sys.exit(EXIT_FAILURE)


def main():
    print("\n=== Export System Setup Verification ===\n")
    test_imports()
    test_template_dir()
    test_required_files()
    test_logo()
    test_reportlab()
    test_python_docx()
    test_pillow()
    print("\nAll checks passed! Export system setup is OK.\n")
    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
