import json

def export_json(errors, output="serpent.json"):
    data = {
        "errors": errors,
        "count": len(errors)
    }

    with open(output, "w") as f:
        json.dump(data, f, indent=2)

    return output
