import json
import re

INPUT_FILE = "data/product_database.txt"
OUTPUT_FILE = "data/product_database.json"


def parse_level_switches_section(lines):
    families = []
    current_family = None
    in_level_switches = False
    in_family = False
    in_notes = False
    in_options = False
    in_base_models = False
    in_spare_parts = False
    for line in lines:
        line = line.rstrip()
        # Detect start of LEVEL SWITCHES section
        if "LEVEL SWITCHES" in line:
            in_level_switches = True
            continue
        if in_level_switches:
            # Detect start of a new family (real family names only)
            if re.match(r"-{10,}", line):
                if current_family and current_family["name"]:
                    families.append(current_family)
                current_family = None
                in_family = False
                in_base_models = False
                in_options = False
                in_notes = False
                in_spare_parts = False
                continue
            # Family name (not Base Models:, not option/adder lines, not section headers, not Notes: or Options:)
            if (
                line
                and not in_family
                and not line.startswith("-")
                and not line.startswith("=")
                and not line.strip().startswith("Base Models:")
                and not line.strip().startswith("*")
                and not line.strip().endswith("add $45/foot")
                and not line.strip().endswith("add $110/foot")
                and not line.strip().startswith("Notes:")
                and not line.strip().startswith("Options:")
            ):
                current_family = {
                    "name": line.strip(),
                    "variants": [],
                    "options": [],
                    "spare_parts": [],
                    "notes": [],
                }
                in_family = True
                in_base_models = False
                in_options = False
                in_notes = False
                in_spare_parts = False
                continue
            # Base Models
            if in_family and line.strip().startswith("Base Models:"):
                in_base_models = True
                in_options = False
                in_notes = False
                in_spare_parts = False
                continue
            # Parse variants (only if in_base_models)
            if in_family and in_base_models and line.strip().startswith("- "):
                m = re.match(r"- ([^:]+): \$(\d+[.]?\d*)", line.strip())
                if m:
                    model = m.group(1)
                    price = float(m.group(2))
                    # Try to extract material, voltage, length from model string
                    material = None
                    voltage = None
                    length = None
                    model_parts = model.split("-")
                    for part in model_parts:
                        if part in ["S", "H", "U", "T", "TS", "CPVC"]:
                            material = part
                        elif "VAC" in part or "VDC" in part:
                            voltage = part
                        elif part.endswith('"'):
                            try:
                                length = int(part.replace('"', ""))
                            except Exception:
                                pass
                    current_family["variants"].append(
                        {
                            "model": model,
                            "base_price": price,
                            "material": material,
                            "voltage": voltage,
                            "length": length,
                        }
                    )
                continue
            # Parse options
            if in_family and line.strip().startswith("Options:"):
                in_options = True
                in_base_models = False
                in_notes = False
                in_spare_parts = False
                continue
            if in_family and in_options and line.strip().startswith("- "):
                # Option with or without adder
                opt_match = re.match(r"- ([^:]+): ADD \$(\d+[.]?\d*)", line.strip())
                if opt_match:
                    opt_name = opt_match.group(1).strip()
                    adder = float(opt_match.group(2))
                    current_family["options"].append({"name": opt_name, "adder": adder})
                else:
                    # Option with adder at end
                    opt_match = re.match(r"- ([^:]+) ADD \$(\d+[.]?\d*)", line.strip())
                    if opt_match:
                        opt_name = opt_match.group(1).strip()
                        adder = float(opt_match.group(2))
                        current_family["options"].append(
                            {"name": opt_name, "adder": adder}
                        )
                    else:
                        # Option with no adder
                        opt_match = re.match(r"- ([^:]+)", line.strip())
                        if opt_match:
                            opt_name = opt_match.group(1).strip()
                            current_family["options"].append({"name": opt_name})
                continue
            # Parse spare parts
            if in_family and line.strip().startswith("Spare Parts:"):
                in_spare_parts = True
                in_options = False
                in_base_models = False
                in_notes = False
                continue
            if in_family and in_spare_parts and line.strip().startswith("- "):
                # Spare part with or without price
                sp_match = re.match(r"- ([^:]+): \$(\d+[.]?\d*)", line.strip())
                if sp_match:
                    part_name = sp_match.group(1).strip()
                    price = float(sp_match.group(2))
                    current_family["spare_parts"].append(
                        {"name": part_name, "price": price}
                    )
                else:
                    sp_match = re.match(r"- ([^:]+)", line.strip())
                    if sp_match:
                        part_name = sp_match.group(1).strip()
                        current_family["spare_parts"].append({"name": part_name})
                continue
            # End spare parts section if next section starts
            if (
                in_family
                and in_spare_parts
                and (
                    line.strip().startswith("Application Notes:")
                    or line.strip().startswith("Notes:")
                )
            ):
                in_spare_parts = False
                in_notes = True
                continue
            # Parse notes
            if in_family and (
                line.strip().startswith("Notes:")
                or line.strip().startswith("Application Notes:")
            ):
                in_notes = True
                in_options = False
                in_base_models = False
                in_spare_parts = False
                continue
            if in_family and in_notes and line.strip().startswith("- "):
                note = line.strip()[2:]
                current_family["notes"].append(note)
                continue
            if in_family and in_notes and re.match(r"\d+\.", line.strip()):
                note = line.strip()
                current_family["notes"].append(note)
                continue
            # End of LEVEL SWITCHES section
            if in_level_switches and "PRESENCE/ABSENCE SWITCHES" in line:
                if current_family and current_family["name"]:
                    families.append(current_family)
                break
    return families


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    families = parse_level_switches_section(lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"families": families}, f, indent=2)
    print(f"Parsed {len(families)} families. Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
