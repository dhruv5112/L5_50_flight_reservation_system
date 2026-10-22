# Lab 5: Static Code Analysis — Flight Reservation System

**Student Name:** Dhruv U  
**SRN:** PES2UG24AM054  
**Department:** Computer Science and Engineering, PES University  
**Course:** Software Engineering Lab (UE24CS252AA2)  
**Assigned Repository:** [SETAPESU26/L5_50_flight_reservation_system](https://github.com/SETAPESU26/L5_50_flight_reservation_system)  
**Main Repository:** [dhruv5112/SE-Lab5](https://github.com/dhruv5112/SE-Lab5)  
**Forked Repository:** [dhruv5112/L5_50_flight_reservation_system](https://github.com/dhruv5112/L5_50_flight_reservation_system)  

---

## Executive Summary & Results

This lab focuses on improving Python code quality, security, and PEP 8 compliance using three complementary static code analysis tools: **Pylint**, **Flake8**, and **Bandit**.

| Static Analysis Tool | Focus Area | Before Fixes | After Fixes | Target / Result |
|---|---|---|---|---|
| **Pylint** | Code quality, design smells, docstrings | `4.00 / 10.00` | **`10.00 / 10.00`** | Target (> 9.5) **Achieved (+6.00 pts)** |
| **Bandit** | Security vulnerabilities (CWE/AST) | 6 issues (2 High, 1 Med, 3 Low) | **0 issues** | **100% Vulnerabilities Remediated** |
| **Flake8** | PEP 8 style, line lengths (<=79), syntax | 10 violations | **0 violations** | **100% PEP 8 Compliant** |

---

## Repository Structure & Deliverables

```
SE_lab5/
├── flight_reservation_system.py  # Cleaned, fully refactored Python program
├── issues.md                     # Completed issues table (14 issues documented)
├── reflection.md                 # Detailed responses to all 4 reflection questions
├── report.pdf                    # Comprehensive 3-page submission report with tables
├── generate_report.py            # Reproducible ReportLab PDF generator script
├── README.md                     # Lab documentation and overview
├── pylint_report.txt             # Current Pylint report (10.00/10)
├── bandit_report.txt             # Current Bandit report (0 issues)
├── flake8_report.txt             # Current Flake8 report (0 violations)
├── reports/                      # Organized archive of historical static analysis logs
│   ├── before/                   # Original reports before remediation
│   │   ├── bandit_report.txt
│   │   ├── flake8_report.txt
│   │   └── pylint_report.txt
│   └── after/                    # Final reports confirming clean status
│       ├── bandit_report.txt
│       ├── flake8_report.txt
│       └── pylint_report.txt
└── .gitignore                    # Excludes venv/, cache, and generated manifests
```

---

## Summary of Remediated Issues

1. **Insecure `eval()` (`B307` / CWE-78):** Replaced dangerous dynamic evaluation with safe parameter parsing and numeric multipliers.
2. **Weak MD5 Hash (`B324` / `B303` / CWE-327):** Upgraded to cryptographically secure SHA-256 (`hashlib.sha256`).
3. **Shell Command Injection (`B605` / `B607` / CWE-78):** Eliminated external shell invocation via `os.system`; replaced with native Python printing.
4. **Predictable PRNG (`B311` / CWE-330):** Replaced standard `random.randint` with CSPRNG `secrets.SystemRandom().randint(1000, 9999)` for boarding PINs.
5. **Hardcoded Sensitive Secret (`B105` / CWE-259):** Refactored API secret retrieval to use environment variables (`os.getenv`).
6. **Broad Bare Except (`B110`, `W0702`, `E722`):** Replaced `except: pass` with explicit `KeyError` handling and meaningful return status.
7. **Dangerous Mutable Default Argument (`W0102`):** Changed `baggage_tags=[]` to `baggage_tags=None` with local initialization.
8. **Global Variable Mutation (`W0603`):** Removed `global total_revenue` by encapsulating financial state within `FINANCIALS["total_revenue"]`.
9. **Unused Imports and Variables (`F401`, `F841`, `W0611`, `W0612`):** Removed `import math`, `airport_fee`, `base_fare`, and unused loop variables.
10. **Line Length Exceeded (`E501`, `C0301`):** Formatted dictionary literals and string interpolations to remain strictly within 79 characters.
11. **Non-PEP 8 Naming Conventions (`C0103`):** Converted function names to standard `snake_case` and constants to `UPPER_CASE`.
12. **Missing Module & Function Docstrings (`C0114`, `C0116`):** Added comprehensive docstrings detailing descriptions, args, and return types.
13. **Unclosed File Operations (`R1732`, `W1514`):** Wrapped file export operations in `with open(..., encoding="utf-8")` context manager.
14. **Singleton Comparison (`E711`, `C0121`):** Replaced `== None` with identity check `is None`.

---

## How to Verify and Run

### 1. Run the Program
```bash
python3 flight_reservation_system.py
```

### 2. Run Static Analysis Tools
```bash
source venv/bin/activate
pylint flight_reservation_system.py
flake8 flight_reservation_system.py
bandit -r flight_reservation_system.py
```

### 3. Regenerate the PDF Report
```bash
python3 generate_report.py
```
