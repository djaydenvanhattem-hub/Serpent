import time

def filter_logs(lines, level=None, since_seconds=None):
    now = time.time()
    results = []

    for line in lines:
        if level and level not in line:
            continue

        # simpele time filter (uitbreidbaar later)
        if since_seconds:
            # placeholder (later timestamp parsing)
            pass

        results.append(line)

    return results
