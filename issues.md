# Lab 5: Static Code Analysis — Identified Issues & Fixes

**Repository:** `SETAPESU26/L5_50_flight_reservation_system`  
**File Analyzed:** `flight_reservation_system.py`  
**Student Name:** Dhruv U  
**SRN:** PES2UG24AM054  

---

## Static Code Analysis Issues Table

The table below documents the security vulnerabilities, code smells, and style issues detected by Bandit, Flake8, and Pylint, prioritized by severity (High and Medium first).

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Insecure Use of `eval()` (`B307`) | Security (Medium Severity) | 47 | `eval(surcharge_expr)` executed arbitrary string expressions dynamically, enabling Remote Code Execution (RCE) / code injection. | Replaced `eval()` with safe arithmetic parsing: validated numeric types and safely extracted the surcharge multiplier without dynamic code evaluation. |
| Use of Weak Cryptographic Hash MD5 (`B324` / `B303`) | Security (High Severity) | 52 | `hashlib.md5(passenger_id.encode())` used MD5, a cryptographically broken hash algorithm vulnerable to collision attacks (CWE-327). | Upgraded hashing algorithm to cryptographically secure SHA-256 (`hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()`). |
| Insecure Process Execution via Shell (`B605` / `B607`) | Security (High Severity) | 63 | `os.system("echo Boarding manifest printed: " + filename)` invoked system shell with concatenated filename, risking command injection (CWE-78). | Eliminated shell execution entirely; replaced `os.system` with native Python `print(f"Boarding manifest printed: {filename}")`. |
| Weak Pseudo-Random Number Generator for Security (`B311`) | Security (Low Severity) | 56 | `random.randint(1000, 9999)` used Mersenne Twister PRNG, which is predictable and unsuitable for security/boarding tokens (CWE-330). | Replaced `random` with cryptographically secure `secrets.SystemRandom().randint(1000, 9999)`. |
| Hardcoded Sensitive API Secret Token (`B105`) | Security (Low Severity) | 75 | Hardcoded string `airline_api_secret = "AIRLINE_DISPATCH_SECRET_TOKEN_2026"` in source code exposes credentials (CWE-259). | Refactored credential retrieval to use environment variables (`os.getenv("AIRLINE_DISPATCH_TOKEN", ...)`). |
| Overly Broad Bare Exception (`B110`, `W0702`, `E722`) | Bug / Code Smell | 31-32 | Bare `except: pass` in `cancelBooking()` caught all exceptions including `KeyboardInterrupt` and masked unexpected runtime bugs. | Replaced bare `except:` with explicit `KeyError` handling and returned a meaningful boolean status indicating success or failure. |
| Mutable Default Argument (`W0102`) | Bug | 15 | `baggage_tags=[]` default argument created a single shared list across all function invocations, accumulating state between distinct calls. | Set default value to `None` (`baggage_tags=None`) and initialized a new list inside the function body if `baggage_tags is None`. |
| Unused Imports and Variables (`F401`, `F841`, `W0611`, `W0612`) | Code Quality / Style | 4, 36, 46, 68 | `import math`, `airport_fee = 35.0`, `base_fare`, and loop index `f` were defined or imported but never utilized. | Removed `import math` and unused variable assignments; simplified iteration using `.values()`. |
| PEP 8 Line Length Exceeded (`E501`, `C0301`) | Style / Formatting | 7, 8, 9, 23 | Lines exceeded standard 79-character / 100-character limits (line 23 was 132 characters long). | Split dictionary entries across multiple lines and wrapped long strings using formatted parenthesized expressions. |
| Non-PEP 8 Function and Variable Naming (`C0103`) | Code Quality / Style | 12, 15, 27, 35, 45, 51, 55, 59, 66 | Function names were camelCase (`bookFlightSeat`, `cancelBooking`, etc.) and constant `total_revenue` was lowercase. | Renamed functions to standard snake_case (`book_flight_seat`, `cancel_booking`, etc.) and encapsulated financial state in `FINANCIALS`. |
| Missing Module and Function Docstrings (`C0114`, `C0116`) | Documentation | 1, 15, 27, 35, 45, 51, 55, 59, 66, 74 | Neither the module nor any of the defined functions included docstrings explaining purpose, arguments, and return values. | Added comprehensive PEP 257 docstrings for the module and all functions including argument and return type descriptions. |
| Unclosed File Resource & Missing Encoding (`R1732`, `W1514`) | Resource Leak / Quality | 60 | `f = open(filename, "w")` without context manager risk leaving file descriptors open, and platform-default encoding was used. | Wrapped file operations in a context manager with explicit UTF-8 encoding: `with open(filename, "w", encoding="utf-8") as manifest_file:`. |
| Singleton Comparison with Equality Operator (`E711`, `C0121`) | Style / Convention | 37 | Comparison `flights.get(flight_no) == None` violates Python singleton comparison best practices. | Changed comparison to identity check: `flights.get(flight_no) is None`. |
| Redundant If-Else Branches (`R1703`, `R1705`) | Code Smell | 39-42 | `checkSeatAvailability` contained unnecessary `else` after `return` and redundant boolean branching. | Simplified to direct boolean return: `return not FLIGHTS[flight_no]["is_full"]`. |

---

## Summary of Analysis Tools Metrics

| Metric | Before Changes | After Changes | Status |
|---|---|---|---|
| **Pylint Score** | **4.00 / 10** | **10.00 / 10** | **Target (>9.5) Exceeded (+6.00 improvement)** |
| **Bandit Findings** | 6 issues (2 High, 1 Medium, 3 Low) | **0 issues** (0 High, 0 Medium, 0 Low) | **All Vulnerabilities Resolved** |
| **Flake8 Violations** | 10 PEP 8 violations | **0 violations** | **100% Clean PEP 8 Compliance** |
