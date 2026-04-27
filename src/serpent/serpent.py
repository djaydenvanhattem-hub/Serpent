import sys
from serpent.parser import extract_errors
from serpent.grouping import group_multiline
from serpent.exporter import export_json
from serpent.filters import filter_logs

__version__ = "2.0.0"

logfile = sys.argv[1]

flags = sys.argv[2:]

errors = extract_errors(logfile)

# multi-line grouping
errors = group_multiline(errors)

# filters
if "--level=ERROR" in flags:
    errors = filter_logs(errors, level="ERROR")

# export JSON
if "--json" in flags:
    path = export_json(errors)
    print(f"Exported to {path}")

print(f"[Serpent v{__version__}] Found {len(errors)} issues\n")

for e in errors:
    print(e)
