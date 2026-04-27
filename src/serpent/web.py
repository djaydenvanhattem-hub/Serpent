import os
import sys
import time
from flask import Flask, jsonify, render_template, request, send_file, abort
from serpent.parser import compute_stats, extract_logs, identify_level

app = Flask(__name__)
FILE = sys.argv[1]

if not os.path.exists(FILE) or not os.path.isfile(FILE):
    raise SystemExit(f"Error: log file not found: {FILE}")


@app.route("/")
def index():
    stats = compute_stats(FILE)
    return render_template("index.html", logfile=FILE, stats=stats)


@app.route("/api/summary")
def api_summary():
    if not os.path.exists(FILE):
        abort(404)

    stats = compute_stats(FILE)
    stats["path"] = FILE
    stats["size_bytes"] = os.path.getsize(FILE)
    stats["modified"] = os.path.getmtime(FILE)
    stats["modified_iso"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats["modified"]))
    stats["last_refresh"] = time.strftime("%H:%M:%S", time.localtime())
    return jsonify(stats)


@app.route("/api/logs")
def api_logs():
    if not os.path.exists(FILE):
        abort(404)

    limit = min(int(request.args.get("limit", 120)), 2000)
    level = request.args.get("level", "ALL").upper()
    lines = extract_logs(FILE, max_lines=1000)

    parsed = [
        {"text": line, "level": identify_level(line)}
        for line in lines
    ]

    if level != "ALL":
        parsed = [entry for entry in parsed if entry["level"] == level]

    return jsonify(
        {
            "logs": parsed[-limit:],
            "limit": limit,
            "filter": level,
            "total": len(parsed),
        }
    )


@app.route("/download")
def download():
    if not os.path.exists(FILE):
        abort(404)

    return send_file(
        FILE,
        as_attachment=True,
        download_name=os.path.basename(FILE),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
