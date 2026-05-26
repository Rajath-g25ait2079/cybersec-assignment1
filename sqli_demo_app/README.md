# SQL Injection Demo Web App — IIT Jodhpur Cyber Security Assignment

> **⚠️ FOR EDUCATIONAL PURPOSES ONLY** — This application is deliberately vulnerable. Never deploy on a public server.

## Quick Start

```bash
# 1. Install Flask
pip install flask

# 2. Run the app
python app.py

# 3. Open in browser
http://localhost:5000
```

## App Structure

| Route | Page | SQLi Type |
|-------|------|-----------|
| `/` | IIT Jodhpur Homepage | — |
| `/login` | Futurense-styled Login | **In-Band SQLi** (Error-based + Auth bypass) |
| `/profile?id=1` | Student Profile | **In-Band SQLi** (UNION-based) |
| `/search?roll=...` | Student Search | **Blind SQLi** (Boolean + Time-based) |
| `/oob_demo` | Notifications | **Out-of-Band SQLi** (Simulated exfiltration) |
| `/reset_db` | Reset database | Restores original data |

## Database Tables

- `students` — 10 student records with passwords
- `grades` — Course grades
- `admin_users` — 3 admin accounts with secret notes
- `secret_flags` — CTF-style flags for each attack type

## Group Members

1. Khushi Bawistale (G25AIT2052)
2. Shashank Jangid (G25AIT2100)
3. Rajath S M (G25AIT2079)
4. Siddhant Singh (G25AIT2105)
5. Deepanshu Arora (G25AIT2029)
6. Soumya A (G25AIT2111)
7. Shah Tirth Rajeshkumar (G25AIT2121)
