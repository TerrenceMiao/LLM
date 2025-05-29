# This is a function that hashes a date, and generate a new valid date in a given begin and end range.

import datetime
import hashlib

# Function to hash, like SHA-256, a string representation of the date and convert it to an integer
def hash_date_to_int(date):
    date_str = date.isoformat()  # e.g., '2023-05-29'
    hash_bytes = hashlib.sha256(date_str.encode('utf-8')).digest()
    hash_int = int.from_bytes(hash_bytes, 'big')
    return hash_int

# Function to map a hash integer to a valid date within a given start and end range
def hash_to_valid_date(original_date, start_date, end_date):
    hash_int = hash_date_to_int(original_date)

    # Calculate number of days between start and end
    delta_days = (end_date - start_date).days
    # Map hash integer to a number within the delta_days
    offset_days = hash_int % delta_days

    new_date = start_date + datetime.timedelta(days=offset_days)
    return new_date

start_date = datetime.date(1960, 1, 1)
end_date = datetime.date(2004, 12, 31)

original_date = datetime.date(1966, 4, 7)

new_date = hash_to_valid_date(original_date, start_date, end_date)

print(f"Original date: {original_date}")
print(f"Hashed date:   {new_date}")
