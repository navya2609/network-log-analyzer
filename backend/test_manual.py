from extractor import extract_timestamps

log = """
Network connection lost
Observed at 2026-08-14 09:17:31

System backup completed
2026-08-14 10:00:00

09:19:06 | monitoring resumed
"""

result = extract_timestamps(log)

print(result)