from extractor import get_context, is_network_event

log = """
Network connection lost
Observed at 2026-08-14 09:17:31

System backup completed
2026-08-14 10:00:00
"""

lines = log.strip().splitlines()

# Test 1: Network timestamp
network_context = get_context(lines, 1, window=4)

print("Network context:", network_context)
print("Is network event:", is_network_event(network_context))

# Test 2: Backup timestamp
backup_context = get_context(lines, 4, window=4)

print("Backup context:", backup_context)
print("Is network event:", is_network_event(backup_context))