import os
import signal
import subprocess
import sys

PID_FILE = "/tmp/serpent_web.pid"


def read_pid():
    if not os.path.exists(PID_FILE):
        return None
    try:
        with open(PID_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (ValueError, OSError):
        return None


def write_pid(pid):
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(pid))


def remove_pid():
    try:
        os.remove(PID_FILE)
    except OSError:
        pass


def is_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def start_daemon(logfile="/var/log/syslog"):
    if not os.path.isfile(logfile):
        print("[Serpent] log file not found:", logfile)
        return

    existing_pid = read_pid()
    if existing_pid and is_running(existing_pid):
        print(f"[Serpent] daemon already running with pid {existing_pid}")
        return

    cmd = ["nohup", "python3", "-m", "serpent.web", logfile]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        close_fds=True,
    )
    write_pid(process.pid)
    print(f"[Serpent] daemon started in background with pid {process.pid}")


def stop_daemon():
    pid = read_pid()
    if not pid:
        print("[Serpent] no Serpent daemon pid file found")
        return

    if not is_running(pid):
        print(f"[Serpent] no running daemon found for pid {pid}, removing stale pid file")
        remove_pid()
        return

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"[Serpent] stopped daemon pid {pid}")
    except OSError as e:
        print(f"[Serpent] could not stop daemon: {e}")
    finally:
        remove_pid()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "stop":
        stop_daemon()
    elif len(sys.argv) == 2:
        start_daemon(sys.argv[1])
    elif len(sys.argv) == 1:
        start_daemon()
    else:
        print("Usage: python3 daemon.py [logfile] | stop")
