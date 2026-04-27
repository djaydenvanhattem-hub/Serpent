__version__ = "1.0.0"

import sys
from parser import extract_errors

if len(sys.argv) < 2:
  print("Usage: serpent logfile")
  sys.exit(1)

logfile = sys.argv[1]

errors = extract_errors(logfile)

print(f"\n[Serpent] Found {len(errors)} issues:\n")

for e in errors:
    print(e)

with open("log.txt", "w") as f:
  f.write("\n".join(errors))

print("\n[Serpent] Saved to log.txt")
