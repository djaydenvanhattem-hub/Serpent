# 🐍 Serpent v3.2.11

![version](https://img.shields.io/badge/version-3.2.11-green)

Serpent is a lightweight log analyzer that detects:
- Errors
- Panics
- Exceptions
- Critical system failures

It provides:
- CLI mode
- Web dashboard
- Log export system

---

## ⚡ Features

- Fast log parsing
- Real-time optional web dashboard
- Error filtering system
- Export to log.txt
- Works on any Linux server

---

## 📦 Installation

Run the installation script with sudo:

```bash
sudo bash install.sh
```

This will:
1. Create a `serpent` system user
2. Clone the repository
3. Install Python dependencies (Flask)
4. Set up global commands: `serpent`, `start77`, `kill77`
5. Configure system PATH for the new user

**Important**: After installation, the `serpent` user needs to log in fresh for the PATH changes to take effect (or run `source ~/.bashrc`).

## 🌐 Web Dashboard

### Option 1: Direct web mode
Analyze a log file and start the web dashboard:

```bash
serpent /var/log/syslog --web
```

Then open your browser to: `http://localhost:8080`

### Option 2: Background daemon mode
Start the dashboard in the background (default file: syslog):

```bash
start77 /var/log/syslog
```

Stop the background dashboard:

```bash
kill77
```

## 📌 CLI Mode

Analyze a log file from the command line:

```bash
serpent /var/log/syslog
serpent /path/to/custom.log
```