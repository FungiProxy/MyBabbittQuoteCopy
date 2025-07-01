#!/usr/bin/env python3
"""
Simple OCR script to extract text from template PNG images using pytesseract
"""

import os
import json
from pathlib import Path
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """Extract text from image using pytesseract"""
    try:
        print(f"Processing: {image_path.name}")
        
        # Open image and convert to RGB if needed
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image)
        
        return text.strip()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

def parse_filename(filename):
    """Parse template filename to extract product family and material"""
    name = filename.replace('.png', '').lower()
    
    product_family = None
    material = None
    variant = None
    
    if 'fs10000' in name:
        product_family = 'FS10000'
    elif 'ls2000' in name:
        product_family = 'LS2000'
        if 'h' in name:
            material = 'HALAR'
        elif 's' in name:
            material = 'Stainless Steel'
    elif 'ls2100' in name:
        product_family = 'LS2100'
        if 'h' in name:
            material = 'HALAR'
        elif 's' in name:
            material = 'Stainless Steel'
    elif 'ls6000' in name:
        product_family = 'LS6000'
        if 'h' in name:
            material = 'HALAR'
        elif 's' in name:
            material = 'Stainless Steel'
    elif 'ls7000' in name:
        if '-2' in name:
            product_family = 'LS7000-2'
            material = 'HALAR'
        else:
            product_family = 'LS7000'
            if 'h' in name:
                material = 'HALAR'
            elif 's' in name:
                material = 'Stainless Steel'
    elif 'ls7500' in name:
        product_family = 'LS7500'
        if 'fullring' in name:
            variant = 'Full Ring'
        elif 'partialring' in name:
            variant = 'Partial Ring'
    elif 'ls8000' in name:
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
    elif 'ls8500' in name:
        product_family = 'LS8500'
        if 'fullring' in name:
            variant = 'Full Ring'
        elif 'partialring' in name:
            variant = 'Partial Ring'
    elif 'lt9000' in name:
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
    print("Starting simple OCR extraction...")
    
    # Find PNG files
    ogtemps_dir = Path('data/ogtemps')
    png_files = list(ogtemps_dir.glob('*.png'))
    
    if not png_files:
        print("No PNG files found!")
        return
    
    print(f"Found {len(png_files)} PNG files")
    
    # Extract data
    results = []
    for png_file in png_files:
        info = parse_filename(png_file.name)
        text = extract_text_from_image(png_file)
        
        if text:
            results.append({
                'filename': png_file.name,
                'product_family': info['product_family'],
                'material': info['material'],
                'variant': info['variant'],
                'text_length': len(text),
                'extracted_text': text
            })
            print(f"  Extracted {len(text)} characters")
        else:
            print(f"  No text extracted")
    
    # Save results
    output_dir = Path('extracted_template_data')
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON
    with open(output_dir / 'simple_extraction.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save individual files
    for result in results:
        filename = result['filename'].replace('.png', '.txt')
        with open(output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(f"Template: {result['filename']}\n")
            f.write(f"Product Family: {result['product_family']}\n")
            f.write(f"Material: {result['material']}\n")
            f.write(f"Variant: {result['variant']}\n")
            f.write("="*50 + "\n\n")
            f.write(result['extracted_text'])
    
    print(f"\n=== EXTRACTION COMPLETE ===")
    print(f"Processed {len(results)} templates successfully")
    print(f"Results saved to: {output_dir}")
    
    # Quick summary
    families = set()
    materials = set()
    for result in results:
        if result['product_family']:
            families.add(result['product_family'])
        if result['material']:
            materials.add(result['material'])
    
    print(f"Product families found: {sorted(families)}")
    print(f"Materials found: {sorted(materials)}")

if __name__ == "__main__":
    main() 