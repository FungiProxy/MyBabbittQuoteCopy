#!/usr/bin/env python3
"""
Update Application Notes
Updates application notes for all product families with comprehensive technical information.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel

def update_application_notes():
    """Update application notes for all product families."""
    
    db = SessionLocal()
    try:
        print("=== UPDATING APPLICATION NOTES ===\n")
        
        # Get all base models
        base_models = db.query(BaseModel).all()
        
        # Application notes for each product family
        app_notes = {
            "LS2000": """1. LS2000 has limited static protection, and is not recommended for plastic pellets or resins with static charges unless extra static option is specified. For extra static protection, ADD $30.00.
2. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.""",
            
            "LS2100": """1. The LS2100 is a loop powered switch that operates between 8mA and 16mA.
2. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.""",
            
            "LS6000": """1. Delrin insulators are standard for SS probes. Teflon insulators are standard for Halar and Teflon Sleeve probes as well as other baked coatings.
2. Max Temperatures are: Delrin insulator 250F; Teflon insulator 450F; PEEK insulator 550F
3. Do not use Delrin in applications with STEAM.
4. Cable probes and special materials of construction available.
5. 3⁄4" NPT process connection is optional at no extra charge ( 3⁄4" NPT Max 300 psi @ 75F)
6. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.""",
            
            "LS7000": """1. Cable probes and special materials of construction available.
2. 3⁄4" NPT process connection is optional at no extra charge ( 3⁄4" NPT Max 300 psi @ 75F)
3. Max Temp for Teflon Insulator 450F, PEEK Insulator 550F.
4. On board timer often used to pump down sumps or avoid nuisance alarms due to splashing.
5. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 72", USE TEFLON SLEEVE.""",
            
            "LS7000/2": """1. VERY IMPORTANT LS 7000/2 IS DESIGNED TO AUTOMATICALLY FILL OR AUTOMATICALLY EMPTY A VESSEL. LS 7000/2 HAS ONLY ONE RELAY, AND THIS RELAY IS DEDICATED TO THE AUTO FILL OR AUTO EMPTYING APPLICATION. It will not give two discrete outputs as is needed to turn on two lights.
2. LS 7000/2 IS DESIGNED TO WORK IN HOMOGENEOUS LIQUIDS. Liquids that change in conductivity or applications where various materials may be in the vessel at different times are undesirable applications. If this is the case, please use two probes.
3. LS 7000/2 MUST HAVE A HALAR COATED PROBE IN ELECTRICALLY CONDUCTIVE LIQUIDS. Water and water based liquids are electrically conductive.
4. LS 7000/2 MUST BE GROUNDED TO THE LIQUID FOR BEST REPEATABILITY. If the unit is screwed into the top of a metal tank, the unit will be properly grounded. If the tank is made of fiberglass, or other non-metallic material, special grounding provisions may be necessary.
5. MATERIAL STICKING ON PROBE WILL AFFECT SETPOINT REPEATABILITY. If this will be a problem, please use two probes instead of LS 7000/2.
6. FOR CRITICAL FILLING APPLICATIONS, A SEPARATE INDEPENDEDNT HIGH LEVEL SWITCH IS RECOMMENDED FOR POSITIVE ALARM AND/OR SHUT DOWN. Changes in the liquid composition could cause the upper set-point to drift. Please be safe by using a back-up level switch for positive shut off in critical applications.
7. DOES NOT WORK WELL IN DRY MATERIALS!
8. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.""",
            
            "LS8000": """1. Remote mounted LS 8000 receiver is normally sold without an enclosure. Enclosures can be purchased as an option.
2. Transmitters for LS 8000 come in several sensitivities. The factory normally matches the sensitivity to the application and probe length. Please specify sensitivity or serial number when ordering replacement transmitters.
3. Transmitter sensitivities are noted in the upper right-hand corner of the transmitter. The designation is as follows:
HI....................................HIGH
M/H..................................MEDIUM HIGH
MED.................................MEDIUM
LO....................................LOW
LLLO.................................TRIPLE LOW
XLO..................................EXTRA LOW
4. Transmitters come in two sizes, one for the standard LS 8000 housing (3/4"NPT process connection), and one for the LS7000 housing (1"NPT process connection). The transmitters for the LS 8000 housing we call "small", and the ones for the LS 7000 housing we call "big". The "big" style transmitters have a blue wire connecting the banana plug to the transmitter.
5. Cable probes and special materials of construction available.
6. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.""",
            
            "LS8000/2": """1. With two receiver cards you can get 4 set points in an LS 8000/2 system on one probe. As this system can have a central point of failure (the transmitter), it is good engineering practice to use a separate independent high level switch for emergency shut-down in critical applications.
2. When using a system with 2 or 4 set points on one probe, please keep in mind that these systems are designed for homogeneous liquids that do not change in their make-up or conductivity. If these conditions exist, please consider using 2 separate probes.
3. For multiple points on one probe, the fluid must be grounded to the mounting nipple. Special consideration should be taken for non-metallic tanks.
4. Applications with water based or electrically conductive liquids must have a Halar coated probe.
5. Material sticking on the probe will affect the repeatability of set points in multiple-point-on-one-probe applications. If such a condition is expected, please use one probe for each set-point.
6. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.""",
            
            "LT9000": """1. It is always good engineering practice to provide a separate, independent high level alarm. 
2. THE LT 9000 IS DESIGNED TO BE USED IN ELECTRICALLY CONDUCTIVE LIQUIDS THAT DO NOT LEAVE A RESIDUE ON THE PROBE. A wet electrically conductive coating will give an indication of level at the highest point that there is a continuous coating from the surface of the fluid.
3. The LT 9000 will give a varying output, if the conductivity of the material changes.
4. For proper operation, the LT 9000 must be grounded to the fluid. In non-metallic tanks, extra grounding provisions may be necessary.
5. LONGEST PROBE WITH HALAR COATING IS 96" (8 FEET). FOR PROBES OVER 96", USE TEFLON SLEEVE.
6. For high temperatures or harsh acids, please check with the factory to see if the epoxy will be compatible with the application.""",
            
            "LS7500": """1. These units are replacement units for Princo P/N's L3515 and L3545. The LS7500 replaces L3515 and the LS8500 replaces L3545.
2. Standard flanges are 316SS Flat Face Flanges.""",
            
            "LS8500": """1. These units are replacement units for Princo P/N's L3515 and L3545. The LS7500 replaces L3515 and the LS8500 replaces L3545.
2. Standard flanges are 316SS Flat Face Flanges.""",
            
            "FS10000": """Max. -probe length recommended is 24".
For detecting emissions before they are visible, we recommend air velocities in excess of 2000 feet per minute.

                                                                          CFM
VELOCITY IN FEET PER MINUTE = _______________________________________
                                                                            2
                                                           (Duct Dia. In Feet) X .78""",
            
            "TRAN-EX": """TRAN-EX application notes to be determined based on specific requirements."""
        }
        
        updated_count = 0
        
        for model in base_models:
            family_name = model.product_family.name if model.product_family else 'Unknown'
            
            if family_name in app_notes:
                model.application_notes = app_notes[family_name]
                updated_count += 1
                print(f"✓ {model.model_number}: Updated application notes")
            else:
                print(f"✗ {model.model_number}: No application notes found for family '{family_name}'")
        
        if updated_count > 0:
            db.commit()
            print(f"\nSuccessfully updated {updated_count} application notes")
        else:
            print("\nNo application notes were updated")
        
        # Show summary
        print("\n=== APPLICATION NOTES SUMMARY ===")
        for model in base_models:
            family_name = model.product_family.name if model.product_family else 'Unknown'
            app_notes = getattr(model, 'application_notes', None)
            if app_notes:
                print(f"• {model.model_number}: {len(app_notes)} characters")
            else:
                print(f"• {model.model_number}: No application notes")
        
    except Exception as e:
        print(f"Error updating application notes: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_application_notes() 