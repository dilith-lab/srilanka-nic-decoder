# srilanka_nic_decoder.py
"""
srilanka_nic_decoder — small utility to decode Sri Lankan NIC numbers into birth date and gender.

Key design decisions:
- Uses Python's datetime for accurate date arithmetic (leap years, month boundaries).
- Exposes small reusable functions:
    - is_valid_nic()
    - parse_nic_base()
    - nic_to_date()
    - decode_nic() -> returns NICInfo dataclass
- Default NIC day offset is 2 (as discovered from real NICs). This is configurable.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import re
from typing import Optional, Tuple

__all__ = [
    "NICInfo",
    "is_valid_nic",
    "parse_nic_base",
    "nic_to_date",
    "decode_nic",
    "DEFAULT_NIC_DAY_OFFSET",
]

# If you want to change behavior, change only this constant
DEFAULT_NIC_DAY_OFFSET = 2


@dataclass(frozen=True)
class NICInfo:
    """
    Result object returned by decode_nic.
    - nic_type: "Old NIC" or "New NIC"
    - gender: "Male" or "Female"
    - birth_year: int (e.g., 1991)
    - raw_day_code: int (original 3-digit code from NIC, before female adjustment)
    - day_code: int (after subtracting 500 for females)
    - birth_date: datetime.date
    """
    nic_type: str
    gender: str
    birth_year: int
    raw_day_code: int
    day_code: int
    birth_date: date

    def __repr__(self) -> str:
        return (
            f"NICInfo(nic_type={self.nic_type!r}, gender={self.gender!r}, "
            f"birth_year={self.birth_year}, raw_day_code={self.raw_day_code}, "
            f"day_code={self.day_code}, birth_date={self.birth_date.isoformat()})"
        )


def is_valid_nic(nic: str) -> bool:
    """
    Basic validation for NIC formats:
      - Old NIC: 10 characters, typically 9 digits + letter (V/v/X/x) or 10 characters where first 5 are digits.
      - New NIC: 12 digits (YYYY + 3 day digits + 4 serial)
    This function performs a lightweight check. More advanced checks can be added as needed.
    """
    nic = nic.strip()
    if len(nic) == 10:
        # Accept forms like 912680444V or purely digits; ensure first 5 chars are digits to read year/day.
        return bool(re.match(r"^\d{5}\w{5}$", nic, flags=re.IGNORECASE))
    if len(nic) == 12:
        return nic.isdigit()
    return False


def parse_nic_base(nic: str) -> Tuple[str, int, int]:
    """
    Parse the NIC string and return (nic_type, birth_year, raw_day_code).
    Raises ValueError on invalid NIC.
    - For old NIC (len==10): year from first 2 chars; day_code from chars 2:5
    - For new NIC (len==12): year from first 4 chars; day_code from chars 4:7
    """
    nic = nic.strip()
    if len(nic) == 10:
        # Old NIC: YYDDDxxxxx  (last char often V)
        try:
            year_part = int(nic[0:2])
            raw_day_code = int(nic[2:5])
        except ValueError:
            raise ValueError("Invalid old NIC: expected digits in positions 1-5.")
        birth_year = 2000 + year_part if 0 <= year_part <= 25 else 1900 + year_part
        nic_type = "Old NIC"
        return nic_type, birth_year, raw_day_code

    elif len(nic) == 12:
        # New NIC: YYYYDDDxxxx
        if not nic.isdigit():
            raise ValueError("Invalid new NIC: expected 12 digits.")
        birth_year = int(nic[0:4])
        raw_day_code = int(nic[4:7])
        nic_type = "New NIC"
        return nic_type, birth_year, raw_day_code

    else:
        raise ValueError("Invalid NIC length; expected 10 (old) or 12 (new).")


def nic_to_date(birth_year: int, day_code: int, offset: int = DEFAULT_NIC_DAY_OFFSET) -> date:
    """
    Convert the NIC day code to a real date using datetime.
    - day_code: integer extracted from NIC (already subtract 500 if female)
    - offset: number of days to subtract to align NIC encoding with actual calendar (default 2)
    Returns a datetime.date instance.
    Raises ValueError for out-of-range dates.
    """
    # Adjust day-of-year according to discovered NIC offset
    day_of_year = day_code - offset

    # Expect day_of_year to be zero-based (0 -> Jan 1)
    start = datetime(birth_year, 1, 1)
    try:
        result = (start + timedelta(days=day_of_year)).date()
    except OverflowError as exc:
        raise ValueError("Computed date out of range") from exc
    return result


def decode_nic(nic: str, offset: int = DEFAULT_NIC_DAY_OFFSET) -> NICInfo:
    """
    Decode a Sri Lankan NIC into a NICInfo object.
    - nic: NIC string (old or new)
    - offset: numeric offset applied to NIC day_code (default is 2)
    """
    nic_type, birth_year, raw_day_code = parse_nic_base(nic)

    # Determine gender and adjust day_code for females
    if raw_day_code > 500:
        gender = "Female"
        day_code = raw_day_code - 500
    else:
        gender = "Male"
        day_code = raw_day_code

    # Validate day_code in plausible range
    if day_code < 0 or day_code > 366 + offset + 5:
        # use a permissive upper bound but still flag nonsense numbers
        raise ValueError("NIC day code out of expected range")

    birth_date = nic_to_date(birth_year, day_code, offset=offset)
    return NICInfo(
        nic_type=nic_type,
        gender=gender,
        birth_year=birth_year,
        raw_day_code=raw_day_code,
        day_code=day_code,
        birth_date=birth_date,
    )


# Simple command-line convenience (not run on import)
if __name__ == "__main__":
    import sys

    try:
        nic = input("Enter NIC number: ").strip()
        info = decode_nic(nic)
        print(f"NIC Type: {info.nic_type}")
        print(f"Birth Year: {info.birth_year}")
        print(f"Gender: {info.gender}")
        print("Date of Birth:", info.birth_date.strftime("%d %B %Y"))
    except Exception as e:
        print("Error:", e)
        sys.exit(1)