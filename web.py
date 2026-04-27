from flask import Flask, render_template, send_file
from parser import extract_errors
import sys

app = Flask(__name__)

LOG_FILE = sys.argv[1]

@app.route("/")
def index():
  errors = extract_errors(LOG_FILE)
  return render_template("index.html", errors=errors)

@app.route("/download")
def download():
  errors = extract_errors(LOG_FILE)

  with open("log.txt", "w") as f:
    f.write("\n".join(errors))

  	return send_file("log.txt", as_attachment=True)

app.run(host="0.0.0.0", port=8080)
