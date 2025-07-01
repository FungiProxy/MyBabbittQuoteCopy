#!/usr/bin/env python3
"""
Extract text from all Word template PNG images using OCR.
"""

import os
import json
from pathlib import Path

def install_easyocr():
    """Install EasyOCR if not available"""
    try:
        import easyocr
        return True
    except ImportError:
        print("Installing EasyOCR...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "easyocr"])
        import easyocr
        return True

def extract_text_from_image(image_path, reader):
    """Extract text from a single image using EasyOCR"""
    try:
        print(f"Processing: {image_path}")
        results = reader.readtext(str(image_path))
        
        # Extract text and combine into full text
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > 0.3:  # Filter out low confidence text
                extracted_text.append(text.strip())
        
        return "\n".join(extracted_text)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def parse_template_filename(filename):
    """Parse template filename to extract product family and material"""
    name = filename.replace('.png', '').lower()
    
    product_family = None
    material = None
    variant = None
    
    if name.startswith('fs10000'):
        product_family = 'FS10000'
    elif name.startswith('ls2000'):
        product_family = 'LS2000'
        if 'h' in name:
            material = 'HALAR'
        elif 's' in name:
            material = 'Stainless Steel'
    elif name.startswith('ls2100'):
        product_family = 'LS2100'
        if 'h' in name:
            material = 'HALAR'
        elif 's' in name:
            material = 'Stainless Steel'
    elif name.startswith('ls6000'):
        product_family = 'LS6000'
        if 'h' in name:
            material = 'HALAR'
        elif 's' in name:
            material = 'Stainless Steel'
    elif name.startswith('ls7000'):
        if '-2' in name:
            product_family = 'LS7000-2'
            material = 'HALAR'
        else:
            product_family = 'LS7000'
            if 'h' in name:
                material = 'HALAR'
            elif 's' in name:
                material = 'Stainless Steel'
    elif name.startswith('ls7500'):
        product_family = 'LS7500'
        if 'fullring' in name:
            variant = 'Full Ring'
        elif 'partialring' in name:
            variant = 'Partial Ring'
    elif name.startswith('ls8000'):
        if '-2' in name:
            product_family = 'LS8000-2'
            material = 'HALAR'
        elif 'ceramicinsulator' in name:
            product_family = 'LS8000'
            material = 'Ceramic Insulator'
        else:
            product_family = 'LS8000'
            if 'h' in name:
                material = 'HALAR'
            elif 's' in name:
                material = 'Stainless Steel'
    elif name.startswith('ls8500'):
        product_family = 'LS8500'
        if 'fullring' in name:
            variant = 'Full Ring'
        elif 'partialring' in name:
            variant = 'Partial Ring'
    elif name.startswith('lt9000'):
        product_family = 'LT9000'
        if 'h' in name:
            material = 'HALAR'
        elif 'ts' in name:
            material = 'Teflon Sleeve'
    
    return {
        'product_family': product_family,
        'material': material,
        'variant': variant
    }

def main():
    """Main function to extract text from all template images"""
    print("Starting template data extraction...")
    
    # Install EasyOCR if needed
    install_easyocr()
    import easyocr
    
    # Initialize OCR reader
    print("Initializing OCR reader...")
    reader = easyocr.Reader(['en'])
    
    # Find all PNG files in ogtemps directory
    ogtemps_dir = Path('data/ogtemps')
    png_files = list(ogtemps_dir.glob('*.png'))
    
    if not png_files:
        print("No PNG files found in data/ogtemps directory!")
        return
    
    print(f"Found {len(png_files)} PNG template files")
    
    # Extract data from each template
    extracted_data = {
        'templates': [],
        'product_families': {},
        'materials': set(),
    }
    
    for png_file in png_files:
        print(f"\n=== Processing {png_file.name} ===")
        
        # Parse filename to get product info
        template_info = parse_template_filename(png_file.name)
        
        # Extract text from image
        full_text = extract_text_from_image(png_file, reader)
        
        if not full_text:
            print(f"No text extracted from {png_file.name}")
            continue
        
        # Store template data
        template_data = {
            'filename': png_file.name,
            'product_family': template_info['product_family'],
            'material': template_info['material'],
            'variant': template_info['variant'],
            'extracted_text': full_text
        }
        
        extracted_data['templates'].append(template_data)
        
        # Collect unique values for analysis
        if template_info['product_family']:
            if template_info['product_family'] not in extracted_data['product_families']:
                extracted_data['product_families'][template_info['product_family']] = {
                    'materials': set(),
                    'templates': []
                }
            
            family_data = extracted_data['product_families'][template_info['product_family']]
            if template_info['material']:
                family_data['materials'].add(template_info['material'])
            family_data['templates'].append(png_file.name)
        
        if template_info['material']:
            extracted_data['materials'].add(template_info['material'])
        
        print(f"Extracted {len(full_text)} characters of text")
    
    # Convert sets to lists for JSON serialization
    for family_name, family_data in extracted_data['product_families'].items():
        family_data['materials'] = list(family_data['materials'])
    
    extracted_data['materials'] = list(extracted_data['materials'])
    
    # Save extracted data to files
    output_dir = Path('extracted_template_data')
    output_dir.mkdir(exist_ok=True)
    
    # Save full extraction results
    with open(output_dir / 'full_extraction.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)
    
    # Save individual template files for easier reading
    for template in extracted_data['templates']:
        filename = template['filename'].replace('.png', '.txt')
        with open(output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(f"Template: {template['filename']}\n")
            f.write(f"Product Family: {template['product_family']}\n")
            f.write(f"Material: {template['material']}\n")
            f.write(f"Variant: {template['variant']}\n")
            f.write("="*50 + "\n\n")
            f.write(template['extracted_text'])
    
    # Create summary report
    with open(output_dir / 'extraction_summary.txt', 'w') as f:
        f.write("TEMPLATE DATA EXTRACTION SUMMARY\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Total templates processed: {len(extracted_data['templates'])}\n")
        f.write(f"Product families found: {len(extracted_data['product_families'])}\n")
        f.write(f"Materials found: {len(extracted_data['materials'])}\n\n")
        
        f.write("PRODUCT FAMILIES:\n")
        for family_name, family_data in extracted_data['product_families'].items():
            f.write(f"  {family_name}: {', '.join(family_data['materials'])}\n")
        
        f.write(f"\nMATERIALS: {', '.join(extracted_data['materials'])}\n")
        
        f.write("\nTEMPLATE FILES:\n")
        for template in extracted_data['templates']:
            f.write(f"  {template['filename']} -> {template['product_family']} / {template['material']}\n")
    
    print(f"\n=== EXTRACTION COMPLETE ===")
    print(f"Processed {len(extracted_data['templates'])} templates")
    print(f"Found {len(extracted_data['product_families'])} product families")  
    print(f"Found {len(extracted_data['materials'])} materials")
    print(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    main() 