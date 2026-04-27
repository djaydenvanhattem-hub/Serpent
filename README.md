# 🐍 Serpent v3.1.19

![version](https://img.shields.io/badge/version-3.1.19-green)

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

```bash
chmod +x Serpent_setup.sh
./Serpent_setup.sh
```

## 🌐 Web dashboard

Start de dashboard met een echt logbestandpad:

```bash
serpent /var/log/syslog --web
```

Open daarna:

```bash
http://127.0.0.1:8080
```

## 📌 Snel starten/stopen

Start met het standaard `syslog`-bestand:

```bash
start77 /var/log/syslog
```

Stop de dashboard met:

```bash
kill77
```