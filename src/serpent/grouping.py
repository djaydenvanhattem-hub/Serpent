import re

ERROR_START = re.compile(r"(ERROR|Exception|Traceback|PANIC|CRITICAL)")

def group_multiline(lines):
    groups = []
    current = []

    for line in lines:
        if ERROR_START.search(line) and current:
            groups.append("\n".join(current))
            current = []

        current.append(line.strip())

    if current:
        groups.append("\n".join(current))

    return groups
