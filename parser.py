import re

PATTERNS = [
  r"ERROR",
  r"CRITICAL",
  r"PANIC",
  r"Exception",
  r"Traceback",
]

def extract_errors(file):
  results = []

  with open(file, "r", errors="ignore") as f:
    for line in f:
      if any(re.search(p, line) for p in PATTERNS):
        results.append(line.strip())

  return results
