#!/usr/bin/env python3
"""
RTF Template Extraction System

This script extracts structured product data from RTF template files and prepares it
for integration into the product database. It parses all RTF files in the template_rtf
directory and extracts key product specifications, pricing information, and configuration
details.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ProductSpecification:
    """Structured product specification data extracted from RTF templates."""
    product_family: str
    material_type: Optional[str] = None
    variant_type: Optional[str] = None
    
    # Core specifications
    supply_voltage: Optional[str] = None
    output_type: Optional[str] = None
    process_connection: Optional[str] = None
    insulator_material: Optional[str] = None
    insulator_length: Optional[str] = None
    insulator_temp_rating: Optional[str] = None
    probe_diameter: Optional[str] = None
    probe_material: Optional[str] = None
    housing_type: Optional[str] = None
    housing_ratings: Optional[str] = None
    
    # Pricing and options
    base_price: Optional[float] = None
    length_adder_per_foot: Optional[float] = None
    length_adder_threshold: Optional[str] = None
    optional_items: Optional[List[Dict[str, Any]]] = None
    
    # Additional specifications
    max_pressure: Optional[str] = None
    warranty_period: Optional[str] = None
    delivery_info: Optional[str] = None
    terms: Optional[str] = None
    
    # Application notes
    application_notes: Optional[str] = None
    special_notes: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.optional_items is None:
            self.optional_items = []
        if self.special_notes is None:
            self.special_notes = []


class RTFTemplateExtractor:
    """Extracts structured data from RTF template files."""
    
    def __init__(self, template_dir: str = "data/template_rtf"):
        self.template_dir = Path(template_dir)
        self.extracted_data = []
    
    def clean_rtf_text(self, text: str) -> str:
        """Clean RTF formatting and extract plain text."""
        # Remove RTF control words and formatting
        text = re.sub(r'\\[a-z]+\d*', '', text)
        text = re.sub(r'\\[{}]', '', text)
        text = re.sub(r'\\\'[0-9a-f]{2}', '', text)
        text = re.sub(r'\\\*\\[a-z]+', '', text)
        text = re.sub(r'\\[a-z]+\s*\{[^}]*\}', '', text)
        
        # Remove font and color tables
        text = re.sub(r'\\fonttbl\{[^}]*\}', '', text)
        text = re.sub(r'\\colortbl\{[^}]*\}', '', text)
        text = re.sub(r'\\stylesheet\{[^}]*\}', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_product_family_and_material(self, filename: str) -> tuple[str, Optional[str], Optional[str]]:
        """Extract product family, material, and variant from filename."""
        name = filename.replace('.rtf', '').lower()
        
        # Map filename patterns to product family and material
        family_material_map = {
            'fs10000': ('FS10000', None, None),
            'ls2000s': ('LS2000', 'Stainless Steel', None),
            'ls2000h': ('LS2000', 'HALAR', None),
            'ls2100s': ('LS2100', 'Stainless Steel', None),
            'ls2100h': ('LS2100', 'HALAR', None),
            'ls6000s': ('LS6000', 'Stainless Steel', None),
            'ls6000h': ('LS6000', 'HALAR', None),
            'ls7000s': ('LS7000', 'Stainless Steel', None),
            'ls7000h': ('LS7000', 'HALAR', None),
            'ls7000-2h': ('LS7000/2', 'HALAR', None),
            'ls7500fullring': ('LS7500', None, 'Full Ring'),
            'ls7500partialring': ('LS7500', None, 'Partial Ring'),
            'ls8000s': ('LS8000', 'Stainless Steel', None),
            'ls8000h': ('LS8000', 'HALAR', None),
            'ls8000ceramicinsulator': ('LS8000', 'Ceramic Insulator', None),
            'ls8000-2h': ('LS8000/2', 'HALAR', None),
            'ls8500fullring': ('LS8500', None, 'Full Ring'),
            'ls8500partialring': ('LS8500', None, 'Partial Ring'),
            'lt9000h': ('LT9000', 'HALAR', None),
            'lt9000ts': ('LT9000', 'Teflon Sleeve', None),
        }
        
        return family_material_map.get(name, (name.upper(), None, None))
    
    def extract_specifications(self, text: str) -> Dict[str, Any]:
        """Extract product specifications from cleaned text."""
        specs = {}
        
        # Extract supply voltage
        voltage_match = re.search(r'Supply Voltage:\s*([^\\\n]+)', text)
        if voltage_match:
            specs['supply_voltage'] = voltage_match.group(1).strip()
        
        # Extract output type
        output_match = re.search(r'Output:\s*([^\\\n]+)', text)
        if output_match:
            specs['output_type'] = output_match.group(1).strip()
        
        # Extract process connection
        connection_match = re.search(r'Process Connection:\s*([^\\\n]+)', text)
        if connection_match:
            specs['process_connection'] = connection_match.group(1).strip()
        
        # Extract insulator information
        insulator_match = re.search(r'Insulator:\s*([^\\\n]+)', text)
        if insulator_match:
            insulator_text = insulator_match.group(1).strip()
            specs['insulator_material'] = insulator_text
            # Extract length and temperature rating
            length_match = re.search(r'(\d+(?:\.\d+)?)\s*["\']?\s*Long\s*\(([^)]+)\)', insulator_text)
            if length_match:
                specs['insulator_length'] = length_match.group(1)
                specs['insulator_temp_rating'] = length_match.group(2)
        
        # Extract probe information
        probe_match = re.search(r'Probe:\s*([^\\\n]+)', text)
        if probe_match:
            probe_text = probe_match.group(1).strip()
            specs['probe_material'] = probe_text
            # Extract diameter
            diameter_match = re.search(r'(\d+(?:/\d+)?)\s*["\']?\s*Diameter', probe_text)
            if diameter_match:
                specs['probe_diameter'] = diameter_match.group(1)
            # If insulator fields are missing, try to extract from probe
            if not specs.get('insulator_material'):
                # Look for pattern like 'Teflon, 4" Long (450 F)'
                probe_ins_match = re.search(r'([A-Za-z0-9\- ]+),\s*(\d+(?:\.\d+)?)\s*["\']?\s*Long\s*\(([^)]+)\)', probe_text)
                if probe_ins_match:
                    specs['insulator_material'] = probe_ins_match.group(1).strip()
                    specs['insulator_length'] = probe_ins_match.group(2)
                    specs['insulator_temp_rating'] = probe_ins_match.group(3)
        
        # Extract housing information
        housing_match = re.search(r'Housing:\s*([^\\\n]+)', text)
        if housing_match:
            housing_text = housing_match.group(1).strip()
            specs['housing_type'] = housing_text
            
            # Extract NEMA ratings
            nema_match = re.search(r'NEMA\s+([^,]+)', housing_text)
            if nema_match:
                specs['housing_ratings'] = nema_match.group(1)
        
        # Extract warranty period
        warranty_match = re.search(r'(\d+)\s*[-]?\s*Year\s*Warranty', text)
        if warranty_match:
            specs['warranty_period'] = warranty_match.group(1)
        
        # Extract max pressure
        pressure_match = re.search(r'(\d+)\s*PSI\s*Max', text)
        if pressure_match:
            specs['max_pressure'] = pressure_match.group(1)
        
        # Extract length adder information
        adder_match = re.search(r'add\s*\$?\s*([\d,]+\.?\d*)\s*per\s*foot', text, re.IGNORECASE)
        if adder_match:
            specs['length_adder_per_foot'] = float(adder_match.group(1).replace(',', ''))
        
        # Extract delivery and terms
        delivery_match = re.search(r'Delivery:\s*([^\\\n]+)', text)
        if delivery_match:
            specs['delivery_info'] = delivery_match.group(1).strip()
        
        terms_match = re.search(r'Terms:\s*([^\\\n]+)', text)
        if terms_match:
            specs['terms'] = terms_match.group(1).strip()
        
        # Extract optional items and pricing
        optional_items = []
        optional_section = re.search(r'\*\*\*\s*Optional\s*\*\*\*.*?(?=Delivery:|$)', text, re.DOTALL | re.IGNORECASE)
        if optional_section:
            optional_text = optional_section.group(0)
            # Look for pricing patterns
            price_matches = re.findall(r'(\$?\s*[\d,]+\.?\d*)\s*EACH', optional_text)
            for price in price_matches:
                optional_items.append({
                    'description': 'Optional item',
                    'price': float(price.replace('$', '').replace(',', ''))
                })
        
        specs['optional_items'] = optional_items
        
        # Extract application notes
        app_notes_match = re.search(r'APPLICATION NOTES.*?(?=Please contact|$)', text, re.DOTALL | re.IGNORECASE)
        if app_notes_match:
            specs['application_notes'] = app_notes_match.group(0).strip()
        
        # Extract special notes
        special_notes = []
        notes_section = re.search(r'Notes:.*?(?=Delivery:|$)', text, re.DOTALL)
        if notes_section:
            notes_text = notes_section.group(0)
            # Split by bullet points or new lines
            note_lines = re.split(r'[•·\-\*]\s*', notes_text)
            for line in note_lines:
                line = line.strip()
                if line and not line.startswith('Notes:'):
                    special_notes.append(line)
        
        specs['special_notes'] = special_notes
        
        return specs
    
    def extract_from_file(self, filepath: Path) -> ProductSpecification:
        """Extract product specification from a single RTF file."""
        print(f"Processing: {filepath.name}")
        
        # Read and clean the RTF content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            rtf_content = f.read()
        
        cleaned_text = self.clean_rtf_text(rtf_content)
        
        # Extract basic information from filename
        family, material, variant = self.extract_product_family_and_material(filepath.name)
        
        # Extract detailed specifications
        specs = self.extract_specifications(cleaned_text)
        
        # Create ProductSpecification object
        product_spec = ProductSpecification(
            product_family=family,
            material_type=material,
            variant_type=variant,
            **specs
        )
        
        return product_spec
    
    def extract_all_templates(self) -> List[ProductSpecification]:
        """Extract data from all RTF template files."""
        if not self.template_dir.exists():
            print(f"Template directory not found: {self.template_dir}")
            return []
        
        rtf_files = list(self.template_dir.glob("*.rtf"))
        print(f"Found {len(rtf_files)} RTF template files")
        
        extracted_data = []
        for rtf_file in rtf_files:
            try:
                spec = self.extract_from_file(rtf_file)
                extracted_data.append(spec)
            except Exception as e:
                print(f"Error processing {rtf_file.name}: {e}")
        
        self.extracted_data = extracted_data
        return extracted_data
    
    def save_to_json(self, output_file: str = "extracted_rtf_data.json"):
        """Save extracted data to JSON file."""
        if not self.extracted_data:
            print("No data to save. Run extract_all_templates() first.")
            return
        
        data = [asdict(spec) for spec in self.extracted_data]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Extracted data saved to: {output_file}")
    
    def print_summary(self):
        """Print a summary of extracted data."""
        if not self.extracted_data:
            print("No data extracted. Run extract_all_templates() first.")
            return
        
        print(f"\n{'='*60}")
        print("RTF TEMPLATE EXTRACTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total templates processed: {len(self.extracted_data)}")
        
        # Group by product family
        families = {}
        for spec in self.extracted_data:
            family = spec.product_family
            if family not in families:
                families[family] = []
            families[family].append(spec)
        
        print(f"\nProduct Families found:")
        for family, specs in families.items():
            materials = [s.material_type for s in specs if s.material_type]
            variants = [s.variant_type for s in specs if s.variant_type]
            
            print(f"  {family}:")
            if materials:
                print(f"    Materials: {', '.join(set(materials))}")
            if variants:
                print(f"    Variants: {', '.join(set(variants))}")
            print(f"    Templates: {len(specs)}")
        
        # Show some key specifications
        print(f"\nKey Specifications found:")
        for spec in self.extracted_data[:3]:  # Show first 3 as examples
            print(f"  {spec.product_family}:")
            if spec.supply_voltage:
                print(f"    Voltage: {spec.supply_voltage}")
            if spec.output_type:
                print(f"    Output: {spec.output_type}")
            if spec.process_connection:
                print(f"    Connection: {spec.process_connection}")
            if spec.insulator_material:
                print(f"    Insulator: {spec.insulator_material}")
            if spec.length_adder_per_foot:
                print(f"    Length Adder: ${spec.length_adder_per_foot}/ft")


def main():
    """Main execution function."""
    extractor = RTFTemplateExtractor()
    
    print("RTF Template Extraction System")
    print("=" * 40)
    
    # Extract all templates
    extracted_data = extractor.extract_all_templates()
    
    if extracted_data:
        # Save to JSON
        extractor.save_to_json()
        
        # Print summary
        extractor.print_summary()
    else:
        print("No templates were processed successfully.")


if __name__ == "__main__":
    main() 