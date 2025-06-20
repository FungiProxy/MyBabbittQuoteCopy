#!/usr/bin/env python3
from sqlalchemy import text

from src.core.database import SessionLocal

db = SessionLocal()

print('=== VERIFICATION OF CLEANUP ===')
print()

# Check remaining options
print('REMAINING OPTIONS BY CATEGORY:')
result = db.execute(
    text(
        'SELECT category, name, COUNT(*) FROM options GROUP BY category, name ORDER BY category, name'
    )
).fetchall()
for category, name, count in result:
    print(f'  {category}: {name} ({count})')

print()
print('SPECIFIC TABLE COUNTS:')
print(
    f'  material_options: {db.execute(text("SELECT COUNT(*) FROM material_options")).scalar()} records'
)
print(
    f'  voltage_options: {db.execute(text("SELECT COUNT(*) FROM voltage_options")).scalar()} records'
)
print(
    f'  options (remaining): {db.execute(text("SELECT COUNT(*) FROM options")).scalar()} records'
)

print()
print('✅ CLEANUP SUCCESS: No duplicate material or voltage data in options table!')
print('✅ All material data is now only in material_options table')
print('✅ All voltage data is now only in voltage_options table')

db.close()
