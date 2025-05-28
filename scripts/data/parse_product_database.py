import re
import json

INPUT_FILE = 'data/product_database.txt'
OUTPUT_FILE = 'data/product_database.json'


def parse_level_switches_section(lines):
    families = []
    current_family = None
    in_level_switches = False
    in_family = False
    for line in lines:
        line = line.rstrip()
        # Detect start of LEVEL SWITCHES section
        if 'LEVEL SWITCHES' in line:
            in_level_switches = True
            continue
        if in_level_switches:
            # Detect start of a new family
            if re.match(r'-{10,}', line):
                if current_family:
                    families.append(current_family)
                current_family = None
                in_family = False
                continue
            # Family name
            if line and not in_family and not line.startswith('-') and not line.startswith('='):
                current_family = {
                    'name': line.strip(),
                    'variants': [],
                    'options': [],
                    'notes': []
                }
                in_family = True
                continue
            # Base Models
            if in_family and line.strip().startswith('Base Models:'):
                in_base_models = True
                continue
            # Parse variants
            if in_family and line.strip().startswith('- '):
                m = re.match(r'- ([^:]+): \$(\d+[.]?\d*)', line.strip())
                if m:
                    model = m.group(1)
                    price = float(m.group(2))
                    # Try to extract material, voltage, length from model string
                    material = None
                    voltage = None
                    length = None
                    model_parts = model.split('-')
                    for part in model_parts:
                        if part in ['S', 'H', 'U', 'T', 'TS', 'CPVC']:
                            material = part
                        elif 'VAC' in part or 'VDC' in part:
                            voltage = part
                        elif part.endswith('"'):
                            try:
                                length = int(part.replace('"', ''))
                            except Exception:
                                pass
                    current_family['variants'].append({
                        'model': model,
                        'base_price': price,
                        'material': material,
                        'voltage': voltage,
                        'length': length
                    })
                continue
            # Parse options
            if in_family and line.strip().startswith('Options:'):
                in_options = True
                continue
            if in_family and 'Spare Parts:' in line:
                in_options = False
                continue
            if in_family and 'Application Notes:' in line:
                in_options = False
                in_notes = True
                continue
            if in_family and line.strip().startswith('- ') and 'ADD' in line and in_options:
                # Option with adder
                opt_match = re.match(r'- ([^:]+): ADD \$(\d+[.]?\d*)', line.strip())
                if opt_match:
                    opt_name = opt_match.group(1).strip()
                    adder = float(opt_match.group(2))
                    current_family['options'].append({'name': opt_name, 'adder': adder})
                else:
                    # Option with adder at end
                    opt_match = re.match(r'- ([^:]+)\s*ADD \$(\d+[.]?\d*)', line.strip())
                    if opt_match:
                        opt_name = opt_match.group(1).strip()
                        adder = float(opt_match.group(2))
                        current_family['options'].append({'name': opt_name, 'adder': adder})
                continue
            # Parse notes
            if in_family and (line.strip().startswith('Notes:') or line.strip().startswith('Application Notes:')):
                in_notes = True
                continue
            if in_family and in_notes and line.strip().startswith('- '):
                note = line.strip()[2:]
                current_family['notes'].append(note)
                continue
            if in_family and in_notes and re.match(r'\d+\.', line.strip()):
                note = line.strip()
                current_family['notes'].append(note)
                continue
            # End of LEVEL SWITCHES section
            if in_level_switches and 'PRESENCE/ABSENCE SWITCHES' in line:
                if current_family:
                    families.append(current_family)
                break
    return families


def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    families = parse_level_switches_section(lines)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'families': families}, f, indent=2)
    print(f"Parsed {len(families)} families. Output written to {OUTPUT_FILE}")

if __name__ == '__main__':
    main() 