#!/usr/bin/env python3
"""
Clean Up Malformed Special Notes
Removes RTF artifacts and malformed characters from special notes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel
import re

def cleanup_special_notes():
    """Clean up malformed special notes by removing RTF artifacts."""
    
    db = SessionLocal()
    try:
        print("=== CLEANING UP SPECIAL NOTES ===\n")
        
        # Get models with malformed special notes
        models_to_clean = db.query(BaseModel).filter(
            BaseModel.special_notes.isnot(None)
        ).all()
        
        updated_count = 0
        
        for model in models_to_clean:
            special_notes = getattr(model, 'special_notes', None)
            if not special_notes:
                continue
                
            original = special_notes
            cleaned = special_notes
            
            # Remove RTF artifacts
            cleaned = re.sub(r'};?\s*360\s*', '360 ', cleaned)  # Remove }; 360
            cleaned = re.sub(r'};?\s*$', '', cleaned)  # Remove trailing };
            cleaned = re.sub(r'\\\'[A-Z0-9]+', '', cleaned)  # Remove \'B7 etc
            cleaned = re.sub(r'\\{2,}', '', cleaned)  # Remove multiple backslashes
            cleaned = re.sub(r'\\', '', cleaned)  # Remove single backslashes
            cleaned = re.sub(r'-5\s*', ' ', cleaned)  # Remove -5 markers
            cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
            cleaned = cleaned.strip()
            
            if cleaned != original:
                model.special_notes = cleaned
                updated_count += 1
                print(f"✓ {model.model_number}:")
                print(f"  Before: {original[:100]}...")
                print(f"  After:  {cleaned[:100]}...")
                print()
        
        if updated_count > 0:
            db.commit()
            print(f"Successfully cleaned {updated_count} special notes")
        else:
            print("No special notes needed cleaning")
        
        # Show current state of special notes
        print("\n=== CURRENT SPECIAL NOTES STATE ===")
        for model in models_to_clean:
            notes = getattr(model, 'special_notes', None)
            if notes:
                print(f"• {model.model_number}: {notes[:80]}...")
            else:
                print(f"• {model.model_number}: No special notes")
        
    except Exception as e:
        print(f"Error cleaning special notes: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_special_notes() 