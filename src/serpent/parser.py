import re
import time
from collections import Counter, deque
from datetime import datetime

PATTERNS = [
    r"ERROR",
    r"CRITICAL",
    r"PANIC",
    r"WARNING",
    r"Exception",
    r"Traceback",
]

LEVEL_KEYWORDS = [
    ("CRITICAL", "CRITICAL"),
    ("PANIC", "PANIC"),
    ("ERROR", "ERROR"),
    ("Traceback", "EXCEPTION"),
    ("Exception", "EXCEPTION"),
    ("WARNING", "WARNING"),
    ("WARN", "WARNING"),
    ("INFO", "INFO"),
    ("DEBUG", "DEBUG"),
]

TIMESTAMP_PATTERNS = [
    r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})",
    r"(?P<ts>\d{2}:\d{2}:\d{2})",
]

TASK_PATTERN = re.compile(r"\b(task|scan|enumeration)\b", flags=re.I)
TASK_COMPLETED = re.compile(r"(completed|successfully|finished)", flags=re.I)
TASK_RUNNING = re.compile(r"(running|starting|started|in progress)", flags=re.I)
MODULE_PATTERN = re.compile(r"Module ['\"]?([A-Za-z0-9_\- ]+)['\"]? loaded", flags=re.I)
TARGET_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def identify_level(line):
    text = line or ""
    for token, level in LEVEL_KEYWORDS:
        if token in text:
            return level
    return "OTHER"


def parse_timestamp(line):
    for pattern in TIMESTAMP_PATTERNS:
        match = re.search(pattern, line)
        if not match:
            continue
        ts = match.group("ts")
        try:
            if len(ts) == 8:
                return datetime.strptime(ts, "%H:%M:%S")
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return None


def format_duration(seconds):
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if days:
        return f"{days}d {hours}h {minutes}m"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {secs}s"


def extract_errors(file):
    results = []
    with open(file, "r", errors="ignore") as f:
        for line in f:
            if any(re.search(p, line) for p in PATTERNS):
                results.append(line.strip())
    return results


def extract_logs(file, max_lines=None):
    with open(file, "r", errors="ignore") as f:
        if max_lines:
            return [line.rstrip("\n") for line in deque(f, max_lines)]
        return [line.rstrip("\n") for line in f]


def compute_stats(file):
    total_lines = 0
    level_counts = Counter()
    pattern_counts = Counter()
    tasks_total = 0
    tasks_running = 0
    tasks_completed = 0
    targets = set()
    modules = set()
    first_ts = None
    last_ts = None

    with open(file, "r", errors="ignore") as f:
        for line in f:
            total_lines += 1
            level = identify_level(line)
            level_counts[level] += 1

            for pattern in PATTERNS:
                if re.search(pattern, line):
                    pattern_counts[pattern] += 1

            if TASK_PATTERN.search(line):
                tasks_total += 1
            if TASK_COMPLETED.search(line):
                tasks_completed += 1
            if TASK_RUNNING.search(line):
                tasks_running += 1

            targets.update(TARGET_PATTERN.findall(line))

            module_match = MODULE_PATTERN.search(line)
            if module_match:
                modules.add(module_match.group(1).strip())

            ts = parse_timestamp(line)
            if ts:
                if first_ts is None or ts < first_ts:
                    first_ts = ts
                if last_ts is None or ts > last_ts:
                    last_ts = ts

    error_lines = (
        level_counts["ERROR"]
        + level_counts["CRITICAL"]
        + level_counts["PANIC"]
        + level_counts["EXCEPTION"]
    )

    uptime = "n.v.t."
    if first_ts and last_ts and last_ts >= first_ts:
        if first_ts.year == 1900 or last_ts.year == 1900:
            uptime = format_duration((last_ts - first_ts).seconds)
        else:
            uptime = format_duration((last_ts - first_ts).total_seconds())

    return {
        "total_lines": total_lines,
        "levels": dict(level_counts),
        "pattern_counts": dict(pattern_counts),
        "error_lines": error_lines,
        "task_total": tasks_total,
        "task_running": tasks_running,
        "task_completed": tasks_completed,
        "targets_count": len(targets),
        "module_count": len(modules),
        "modules": sorted(modules),
        "targets": sorted(targets),
        "uptime": uptime,
    }
