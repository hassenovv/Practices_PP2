from datetime import datetime, timedelta

# 1. Subtract five days from the current date
print("1:", datetime.now() - timedelta(days=5))

# 2. Yesterday, today, tomorrow
today = datetime.now().date()
print("2: yesterday =", today - timedelta(days=1))
print("   today     =", today)
print("   tomorrow  =", today + timedelta(days=1))

# 3. Drop microseconds
print("3:", datetime.now().replace(microsecond=0))

# 4. Difference between two dates in seconds
d1 = datetime(2026, 9, 1, 12, 0, 0)
d2 = datetime(2026, 9, 28, 18, 30, 15)
print("4:", (d2 - d1).total_seconds(), "seconds")
