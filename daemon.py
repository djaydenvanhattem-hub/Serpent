import subprocess
import sys

def start_daemon(logfile):
    cmd = ["nohup", "python3", "web.py", logfile, "&"]

    subprocess.Popen(cmd)

    print("[Serpent] daemon started in background")
