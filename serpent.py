__version__: "1.0.0"

from parser import extract_errors
import sys

__version__ = "1.0.0"

if len(sys.argv) < 2:
    print("Usage: serpent logfile")
    exit()

file = sys.argv[1]

errors = extract_errors(file)

print(f"\n[Serpent v{__version__}] Found {len(errors)} issues:\n")

for e in errors:
    print(e)

with open("log.txt", "w") as f:
    f.write("\n".join(errors))

print("\nSaved to log.txt")
