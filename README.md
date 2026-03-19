# 🔐 Hashcat Password Analysis Tool

A Python script that parses Hashcat cracked output files and generates a detailed analysis of password lengths and character set composition — useful for pentest reporting and password audit findings.

---

## 📋 Features

- Parses both `username:hash:password` and `hash:password` formats automatically
- **Password Length Analysis** — counts and percentages by character length
- **Character Set Analysis** — categorizes passwords by complexity (lowercase, uppercase, numbers, special characters, and combinations)
- **Blank Password Detection** — identifies and lists accounts with no password set
- **Weak Password Detection** — flags accounts with passwords at or under a specified length via `--weak`
- Clean, formatted terminal output ready for screenshots in reports

---

## 📁 Supported Input Formats

Generated from Hashcat using the `--username` flag:
```
Administrator:64f12cddaa88057e06a81b54e73b949b:Password123
jsmith:b4b9b02e6f09a9bd760f388b67351e2b:Summer2023!
```

Or standard Hashcat output without usernames:
```
64f12cddaa88057e06a81b54e73b949b:Password123
b4b9b02e6f09a9bd760f388b67351e2b:Summer2023!
```

---

## 🚀 Usage

**Step 1 — Export cracked results from Hashcat:**
```bash
hashcat -m 1000 hashes.txt rockyou.txt --username --show > cracked.txt
```

**Step 2 — Run the analysis script:**
```bash
python3 hashcat_analysis.py cracked.txt
```

**Optional — Flag accounts with weak passwords using `--weak`:**
```bash
python3 hashcat_analysis.py cracked.txt --weak 8
```

This will flag any account with a password of 8 characters or fewer at the bottom of the output.

---

## 📊 Sample Output

```
=====================================
      Password Length Analysis
=====================================
   Length      Count     % of Total
-------------------------------------
     2           1          1.0%
     3           2          2.0%
     4           1          1.0%
     5           4          4.0%
     6           27        27.3%
     7           19        19.2%
     8           25        25.3%
     9           13        13.1%
     10          3          3.0%
     11          3          3.0%
     12          1          1.0%
-------------------------------------
   Total         99
=====================================

======================================================
           Character Set Analysis
======================================================
  Category                        Count    % of Total
------------------------------------------------------
  Lowercase Only                    47       47.5%
  Uppercase Only                     1        1.0%
  Numbers Only                       2        2.0%
  Lower + Numbers                   20       20.2%
  Mixed Case + Numbers               6        6.1%
  Mixed Case + Numbers + Special    23       23.2%
------------------------------------------------------
  Total                             99
======================================================

*** WARNING: 1 account(s) found with no password set! ***
  Accounts with blank passwords:
    - bjones

*** WARNING: 8 account(s) with passwords <= 5 characters ***
  Username             Password Length
  ------------------ ---------------
  qadams                      2
  mwilliams                   3
  svc_sql                     3
  temp_user                   4
  dsanchez                    5
  lmorris                     5
  BobbyPin                    5
  lhall                       5
```

---

## 🗂️ Character Set Categories

| Category | Example |
|----------|---------|
| Lowercase Only | `password` |
| Uppercase Only | `PASSWORD` |
| Numbers Only | `123456` |
| Lower + Numbers | `abc123` |
| Upper + Numbers | `ABC123` |
| Mixed Case | `PassWord` |
| Mixed Case + Numbers | `Password123` |
| Lower + Special | `password!` |
| Upper + Special | `PASSWORD!` |
| Numbers + Special | `1234!` |
| Mixed Case + Special | `PassWord!` |
| Lower + Numbers + Special | `abc123!` |
| Upper + Numbers + Special | `ABC123!` |
| Mixed Case + Numbers + Special | `Password123!` |
| Special Only | `!!!` |

---

## ⚙️ Requirements

- Python 3.6+
- No external libraries required — standard library only

---

## ⚠️ Disclaimer

This tool is intended for use during **authorized penetration testing and security assessments only**. Always ensure you have written permission before testing any systems or analyzing credentials. Unauthorized use is illegal and unethical.

---

## 📄 License

MIT License — free to use and modify.
