"""
Complete Import and Usage Demo for lka-nic-decoder
Shows all possible ways to import and use the module
"""

print("=" * 60)
print("LKA NIC DECODER - ALL IMPORT METHODS DEMO")
print("=" * 60)

# Test NICs
old_nic = "912680444V"  # Male, 1991-09-24
new_nic = "199253600001"  # Female, 1992-02-05

print("\n1. IMPORT ENTIRE MODULE")
print("-" * 30)
import lka_nic_decoder

info1 = lka_nic_decoder.decode_nic(old_nic)
print(f"Module import: {info1.birth_date} ({info1.gender})")

print("\n2. IMPORT SPECIFIC FUNCTION")
print("-" * 30)
from lka_nic_decoder import decode_nic

info2 = decode_nic(new_nic)
print(f"Function import: {info2.birth_date} ({info2.gender})")

print("\n3. IMPORT MULTIPLE FUNCTIONS")
print("-" * 30)
from lka_nic_decoder import decode_nic, parse_nic_base, nic_to_date

nic_type, year, day_code = parse_nic_base(old_nic)
birth_date = nic_to_date(year, day_code if day_code <= 500 else day_code - 500)
print(f"Multi-import: {nic_type}, {year}, {birth_date}")

print("\n4. IMPORT WITH ALIAS")
print("-" * 30)
from lka_nic_decoder import decode_nic as decode

info4 = decode(old_nic)
print(f"Alias import: {info4.birth_date} ({info4.gender})")

print("\n5. IMPORT ALL (NOT RECOMMENDED)")
print("-" * 30)
from lka_nic_decoder import *

info5 = decode_nic(new_nic)
print(f"Star import: {info5.birth_date} ({info5.gender})")

print("\n6. IMPORT DATACLASS")
print("-" * 30)
from lka_nic_decoder import NICInfo, decode_nic

info6: NICInfo = decode_nic(old_nic)
print(f"Dataclass: {info6.nic_type} - {info6.birth_date}")

print("\n7. IMPORT CONSTANT")
print("-" * 30)
from lka_nic_decoder import DEFAULT_NIC_DAY_OFFSET, nic_to_date

custom_date = nic_to_date(1991, 268, offset=DEFAULT_NIC_DAY_OFFSET)
print(f"Constant import: Offset={DEFAULT_NIC_DAY_OFFSET}, Date={custom_date}")

print("\n8. VALIDATION FUNCTION")
print("-" * 30)
from lka_nic_decoder import is_valid_nic

print(f"Valid old NIC: {is_valid_nic(old_nic)}")
print(f"Valid new NIC: {is_valid_nic(new_nic)}")
print(f"Invalid NIC: {is_valid_nic('invalid')}")

print("\n9. COMPLETE WORKFLOW EXAMPLE")
print("-" * 30)
from lka_nic_decoder import is_valid_nic, decode_nic

def process_nic(nic_number):
    if not is_valid_nic(nic_number):
        return f"Invalid NIC: {nic_number}"
    
    info = decode_nic(nic_number)
    return f"{nic_number} -> {info.birth_date.strftime('%B %d, %Y')} ({info.gender})"

print(process_nic(old_nic))
print(process_nic(new_nic))
print(process_nic("invalid123"))

print("\n10. ERROR HANDLING DEMO")
print("-" * 30)
from lka_nic_decoder import decode_nic

try:
    bad_info = decode_nic("1234567890")  # Valid format but invalid date
    print(f"Decoded: {bad_info.birth_date}")
except ValueError as e:
    print(f"Error caught: {e}")

print("\n" + "=" * 60)
print("ALL IMPORT METHODS DEMONSTRATED SUCCESSFULLY!")
print("=" * 60)