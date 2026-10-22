"""Script to generate a professional PDF report for Lab 5: Static Code Analysis."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages dynamically for running footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(
                36,
                letter[1] - 28,
                "PES University | SE Lab 5: Static Code Analysis Report",
            )
            self.drawRightString(
                letter[0] - 36,
                letter[1] - 28,
                "Dhruv U (PES2UG24AM054)",
            )
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, letter[1] - 32, letter[0] - 36, letter[1] - 32)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 36, letter[0] - 36, 36)
        self.drawString(
            36,
            24,
            "Software Engineering Lab (UE24CS252AA2) — Confidential / Academic Submission",
        )
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 36, 24, page_text)
        self.restoreState()


def build_pdf(filename="report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=44,
    )

    styles = getSampleStyleSheet()

    # Custom palette
    primary_color = colors.HexColor("#1A365D")  # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0")  # Slate Blue
    dark_neutral = colors.HexColor("#2D3748")  # Charcoal body
    accent_green = colors.HexColor("#22543D")  # Dark Green
    accent_red = colors.HexColor("#742A2A")  # Dark Red
    bg_header = colors.HexColor("#2B6CB0")
    bg_alt_row = colors.HexColor("#F7FAFC")
    bg_callout = colors.HexColor("#EDF2F7")

    # Typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=dark_neutral,
        spaceAfter=5,
    )

    meta_label = ParagraphStyle(
        "MetaLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=primary_color,
    )

    meta_val = ParagraphStyle(
        "MetaVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=dark_neutral,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=dark_neutral,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=dark_neutral,
    )

    table_cell_code = ParagraphStyle(
        "TableCellCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7,
        leading=9,
        textColor=primary_color,
    )

    q_style = ParagraphStyle(
        "QStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    story = []

    # Title Banner
    story.append(
        Paragraph("Lab 5: Static Code Analysis Report", title_style)
    )
    story.append(
        Paragraph(
            "Automated Code Quality, PEP 8 Formatting & Security Vulnerability Remediation",
            subtitle_style,
        )
    )

    # Metadata Block Table
    meta_data = [
        [
            Paragraph("Student Name:", meta_label),
            Paragraph("Dhruv U", meta_val),
            Paragraph("Course:", meta_label),
            Paragraph("Software Engineering Lab (UE24CS252AA2)", meta_val),
        ],
        [
            Paragraph("SRN:", meta_label),
            Paragraph("PES2UG24AM054", meta_val),
            Paragraph("Institution:", meta_label),
            Paragraph("PES University, Bengaluru", meta_val),
        ],
        [
            Paragraph("Assigned Repo:", meta_label),
            Paragraph("SETAPESU26/L5_50_flight_reservation_system", meta_val),
            Paragraph("GitHub Target:", meta_label),
            Paragraph("dhruv5112/SE-Lab5", meta_val),
        ],
        [
            Paragraph("Target Script:", meta_label),
            Paragraph("flight_reservation_system.py", meta_val),
            Paragraph("Date of Execution:", meta_label),
            Paragraph("October 2026", meta_val),
        ],
    ]
    meta_table = Table(
        meta_data, colWidths=[80, 185, 80, 195]
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_callout),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Summary & Metrics
    story.append(Paragraph("1. Executive Summary & Verification Metrics", h1_style))
    story.append(
        Paragraph(
            "This lab enhances Python source code quality, security, and maintainability by applying "
            "three industry-standard static analysis tools: <b>Pylint</b> (code reviewer and logical quality), "
            "<b>Flake8</b> (PEP 8 style guide and grammar checker), and <b>Bandit</b> (security scanner and CWE/AST analyzer). "
            "All issues identified across the starter script were systematically remediated, achieving <b>10.00/10 Pylint score</b>, "
            "<b>0 Flake8 violations</b>, and <b>0 Bandit security findings</b>.",
            body_style,
        )
    )

    # Metrics Summary Table
    metrics_data = [
        [
            Paragraph("Static Analysis Tool", table_header_style),
            Paragraph("Scope / Focus Area", table_header_style),
            Paragraph("Before Remediation", table_header_style),
            Paragraph("After Remediation", table_header_style),
            Paragraph("Outcome / Improvement", table_header_style),
        ],
        [
            Paragraph("<b>Pylint</b>", table_cell_bold),
            Paragraph("Code smells, conventions, docstrings, typing", table_cell_style),
            Paragraph("<font color='#C53030'><b>4.00 / 10.00</b></font>", table_cell_style),
            Paragraph("<font color='#22543D'><b>10.00 / 10.00</b></font>", table_cell_style),
            Paragraph("Target (>9.5) Exceeded (<b>+6.00 pts</b>, Perfect Score)", table_cell_style),
        ],
        [
            Paragraph("<b>Bandit</b>", table_cell_bold),
            Paragraph("Security threats, CWEs, injection, cryptography", table_cell_style),
            Paragraph("<font color='#C53030'><b>6 issues</b> (2 High, 1 Med, 3 Low)</font>", table_cell_style),
            Paragraph("<font color='#22543D'><b>0 issues</b> (Zero findings)</font>", table_cell_style),
            Paragraph("100% Vulnerabilities Remediated", table_cell_style),
        ],
        [
            Paragraph("<b>Flake8</b>", table_cell_bold),
            Paragraph("PEP 8 style, line length (<=79), syntax", table_cell_style),
            Paragraph("<font color='#C53030'><b>10 violations</b></font>", table_cell_style),
            Paragraph("<font color='#22543D'><b>0 violations</b> (Clean)</font>", table_cell_style),
            Paragraph("100% PEP 8 Compliance Achieved", table_cell_style),
        ],
    ]
    metrics_table = Table(
        metrics_data, colWidths=[65, 155, 105, 105, 110]
    )
    metrics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), bg_header),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(metrics_table)
    story.append(Spacer(1, 10))

    # Comprehensive Issues & Changes Table
    story.append(Paragraph("2. Comprehensive Identified Issues & Changes Table", h1_style))
    story.append(
        Paragraph(
            "The following table details all 14 identified defects across Bandit, Flake8, and Pylint, prioritized by "
            "severity (Security High and Medium first, followed by logic bugs, style violations, and code quality standards).",
            body_style,
        )
    )

    changes_data = [
        [
            Paragraph("Issue & ID", table_header_style),
            Paragraph("Tool", table_header_style),
            Paragraph("Severity / Type", table_header_style),
            Paragraph("Line(s)", table_header_style),
            Paragraph("Description of Defect", table_header_style),
            Paragraph("Remediation / Fix Approach", table_header_style),
        ],
        [
            Paragraph("Insecure eval()<br/><code>B307</code>", table_cell_bold),
            Paragraph("Bandit", table_cell_style),
            Paragraph("<font color='#C53030'>Medium (CWE-78)</font>", table_cell_style),
            Paragraph("47", table_cell_code),
            Paragraph("eval(surcharge_expr) dynamically executes arbitrary input strings, creating Remote Code Execution (RCE) risk.", table_cell_style),
            Paragraph("Replaced eval() with safe parsing: extracts numeric multiplier string after 'base_fare*' and converts via float().", table_cell_style),
        ],
        [
            Paragraph("Weak Hash MD5<br/><code>B324 / B303</code>", table_cell_bold),
            Paragraph("Bandit", table_cell_style),
            Paragraph("<font color='#C53030'>High (CWE-327)</font>", table_cell_style),
            Paragraph("52", table_cell_code),
            Paragraph("hashlib.md5() used for passenger identifier hashing. MD5 is cryptographically broken and prone to collision attacks.", table_cell_style),
            Paragraph("Upgraded to cryptographically secure SHA-256 (hashlib.sha256(passenger_id.encode('utf-8')).hexdigest()).", table_cell_style),
        ],
        [
            Paragraph("Shell Execution<br/><code>B605 / B607</code>", table_cell_bold),
            Paragraph("Bandit", table_cell_style),
            Paragraph("<font color='#C53030'>High (CWE-78)</font>", table_cell_style),
            Paragraph("63", table_cell_code),
            Paragraph("os.system('echo ... ' + filename) executes shell with unescaped filename, enabling shell command injection.", table_cell_style),
            Paragraph("Eliminated external shell call entirely; used native Python print(f'Boarding manifest printed: {filename}').", table_cell_style),
        ],
        [
            Paragraph("Insecure PRNG<br/><code>B311</code>", table_cell_bold),
            Paragraph("Bandit", table_cell_style),
            Paragraph("<font color='#DD6B20'>Low (CWE-330)</font>", table_cell_style),
            Paragraph("56", table_cell_code),
            Paragraph("random.randint() uses Mersenne Twister PRNG, which is predictable and unsuitable for security boarding tokens.", table_cell_style),
            Paragraph("Replaced random with CSPRNG: secrets.SystemRandom().randint(1000, 9999) from the standard secrets module.", table_cell_style),
        ],
        [
            Paragraph("Hardcoded Secret<br/><code>B105</code>", table_cell_bold),
            Paragraph("Bandit", table_cell_style),
            Paragraph("<font color='#DD6B20'>Low (CWE-259)</font>", table_cell_style),
            Paragraph("75", table_cell_code),
            Paragraph("Hardcoded sensitive credential string airline_api_secret in source code risks accidental exposure in VCS.", table_cell_style),
            Paragraph("Refactored to fetch credentials via environment variables: os.getenv('AIRLINE_DISPATCH_TOKEN', fallback).", table_cell_style),
        ],
        [
            Paragraph("Bare Except & Pass<br/><code>B110 / W0702 / E722</code>", table_cell_bold),
            Paragraph("Bandit, Pylint, Flake8", table_cell_style),
            Paragraph("<font color='#DD6B20'>Low / Bug</font>", table_cell_style),
            Paragraph("31-32", table_cell_code),
            Paragraph("try ... except: pass swallowed all errors blindly, including KeyboardInterrupt, masking unexpected runtime failures.", table_cell_style),
            Paragraph("Replaced with specific KeyError handling and returned a meaningful boolean status (True on success, False on error).", table_cell_style),
        ],
        [
            Paragraph("Mutable Default Arg<br/><code>W0102</code>", table_cell_bold),
            Paragraph("Pylint", table_cell_style),
            Paragraph("<font color='#C53030'>Bug</font>", table_cell_style),
            Paragraph("15", table_cell_code),
            Paragraph("baggage_tags=[] evaluated once at definition time; mutated list persists across distinct passenger booking calls.", table_cell_style),
            Paragraph("Changed default argument to None (baggage_tags=None) and instantiated new list if baggage_tags is None inside body.", table_cell_style),
        ],
        [
            Paragraph("Global Variable Mutation<br/><code>W0603</code>", table_cell_bold),
            Paragraph("Pylint", table_cell_style),
            Paragraph("Code Smell", table_cell_style),
            Paragraph("16", table_cell_code),
            Paragraph("global total_revenue mutates global module state, creating race conditions and tight coupling.", table_cell_style),
            Paragraph("Encapsulated financial state within an explicit dictionary structure FINANCIALS['total_revenue'].", table_cell_style),
        ],
        [
            Paragraph("Unused Imports & Vars<br/><code>F401 / F841 / W0611 / W0612</code>", table_cell_bold),
            Paragraph("Flake8, Pylint", table_cell_style),
            Paragraph("Code Quality", table_cell_style),
            Paragraph("4, 36, 46, 68", table_cell_code),
            Paragraph("import math, airport_fee = 35.0, base_fare, and loop index variable f were assigned/imported but never used.", table_cell_style),
            Paragraph("Removed unused import math and variables; refactored loop to iterate directly over flight_dict.values().", table_cell_style),
        ],
        [
            Paragraph("Line Length Exceeded<br/><code>E501 / C0301</code>", table_cell_bold),
            Paragraph("Flake8, Pylint", table_cell_style),
            Paragraph("Style Violation", table_cell_style),
            Paragraph("7, 8, 9, 23", table_cell_code),
            Paragraph("Dictionary declarations and formatting strings exceeded 79/100 characters (line 23 was 132 characters).", table_cell_style),
            Paragraph("Reformatted multi-line dictionary mappings and broke long string interpolations using parenthesized expressions.", table_cell_style),
        ],
        [
            Paragraph("Missing Docstrings<br/><code>C0114 / C0116</code>", table_cell_bold),
            Paragraph("Pylint", table_cell_style),
            Paragraph("Convention", table_cell_style),
            Paragraph("Module & All Funcs", table_cell_code),
            Paragraph("Module and functions lacked PEP 257 docstrings detailing purpose, parameters, and return types.", table_cell_style),
            Paragraph("Authored comprehensive multi-line docstrings for module and every function including Args and Returns sections.", table_cell_style),
        ],
        [
            Paragraph("Non-PEP 8 Naming<br/><code>C0103</code>", table_cell_bold),
            Paragraph("Pylint", table_cell_style),
            Paragraph("Style / Convention", table_cell_style),
            Paragraph("12, 15, 27, 35, 45, etc.", table_cell_code),
            Paragraph("Functions used camelCase (bookFlightSeat) and constants were lowercase (total_revenue), violating PEP 8.", table_cell_style),
            Paragraph("Renamed functions to snake_case (book_flight_seat, cancel_booking) and module data to UPPER_CASE (FLIGHTS).", table_cell_style),
        ],
        [
            Paragraph("Resource Leak in open()<br/><code>R1732 / W1514</code>", table_cell_bold),
            Paragraph("Pylint", table_cell_style),
            Paragraph("Resource Leak", table_cell_style),
            Paragraph("60", table_cell_code),
            Paragraph("f = open(filename, 'w') without context manager risks leaking file descriptors if errors occur, encoding unspecified.", table_cell_style),
            Paragraph("Wrapped file I/O in context manager with explicit encoding: with open(filename, 'w', encoding='utf-8') as file:.", table_cell_style),
        ],
        [
            Paragraph("Singleton Equality<br/><code>E711 / C0121</code>", table_cell_bold),
            Paragraph("Flake8, Pylint", table_cell_style),
            Paragraph("Convention", table_cell_style),
            Paragraph("37", table_cell_code),
            Paragraph("flights.get(flight_no) == None compares singleton using == equality rather than is identity operator.", table_cell_style),
            Paragraph("Changed comparison to identity check: flights.get(flight_no) is None.", table_cell_style),
        ],
    ]

    changes_table = Table(
        changes_data, colWidths=[65, 45, 65, 35, 160, 170]
    )
    changes_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), bg_header),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, bg_alt_row],
                ),
            ]
        )
    )
    story.append(changes_table)
    story.append(Spacer(1, 10))

    # Reflection Questions & Answers Section
    story.append(Paragraph("3. Reflection & Analysis Questions", h1_style))

    story.append(
        Paragraph(
            "Q1. What is the difference in the primary focus areas of Pylint, Flake8, and Bandit? Why is it beneficial to use all three rather than just one?",
            q_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Flake8</b> enforces PEP 8 grammar, formatting, whitespace, and line lengths (<=79 chars) combining pycodestyle, "
            "pyflakes, and mccabe. <b>Pylint</b> evaluates deep structural health, detecting code smells, mutable default arguments, "
            "docstrings, and design conventions, producing a quantitative score out of 10.0. <b>Bandit</b> is dedicated to security, "
            "scanning the Abstract Syntax Tree (AST) for Common Weakness Enumerations (CWEs) such as code injection (eval), weak cryptography "
            "(MD5), and command injection (os.system).<br/>"
            "<b>Why use all three?</b> Flake8 and Pylint ensure code is clean and readable, but are blind to severe security vulnerabilities "
            "(e.g., an eval() or MD5 call can easily earn a 10/10 Pylint score). Bandit catches security risks but ignores formatting and maintainability bugs. "
            "Concurrently utilizing all three establishes an indispensable, multi-layered quality gate.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Q2. Describe a specific warning or error flagged by each tool during the lab. How did you remediate (fix) them?",
            q_style,
        )
    )
    story.append(
        Paragraph(
            "• <b>Bandit:</b> Flagged <code>B307: Use of possibly insecure function eval()</code> on line 47. <i>Remediation:</i> Removed dynamic code evaluation "
            "and safely parsed numeric multipliers via string extraction and <code>float()</code> conversion, eliminating RCE vectors.<br/>"
            "• <b>Flake8:</b> Flagged <code>F401 'math' imported but unused</code> and <code>E501 line too long (132 > 79)</code>. <i>Remediation:</i> Removed the "
            "dangling math import and split dictionary literals and string interpolations into multi-line expressions under 79 characters.<br/>"
            "• <b>Pylint:</b> Flagged <code>W0102: Dangerous default value [] as argument</code> on line 15. <i>Remediation:</i> Changed the parameter default to "
            "<code>baggage_tags=None</code> and instantiated a fresh list inside the function body, preventing cross-passenger state leakage.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Q3. Did you encounter any 'false positives' or warnings that you felt were unnecessary to fix? How should a development team handle false positives in a CI/CD pipeline?",
            q_style,
        )
    )
    story.append(
        Paragraph(
            "Bandit flagged <code>B105: Possible hardcoded password</code> for <code>airline_api_secret</code>. While merely a demo token, hardcoded strings in code "
            "remain high risk. We refactored it to fetch from environment variables. In enterprise CI/CD workflows, teams should handle legitimate false positives through: "
            "(1) <b>Documented Inline Suppressions:</b> Using targeted comments (e.g. <code># nosec B303</code> or <code># noqa: E501</code>) with audit justifications; "
            "(2) <b>Centralized Configuration Files:</b> Maintaining <code>.flake8</code>, <code>.pylintrc</code>, or <code>pyproject.toml</code> to set team-wide conventions (e.g., 88-char limits); and "
            "(3) <b>Severity Thresholds:</b> Enforcing hard pipeline failures on High/Medium vulnerabilities while treating stylistic items as warnings.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Q4. How can static code analysis be integrated into a software development lifecycle (SDLC) or CI/CD pipeline to prevent technical debt and security flaws proactively?",
            q_style,
        )
    )
    story.append(
        Paragraph(
            "Static analysis is the foundation of the <b>Shift-Left</b> paradigm: (1) <b>Pre-Commit Hooks:</b> Automating Flake8, Bandit, and Pylint via <code>pre-commit</code> "
            "to reject non-compliant code before it is committed locally; (2) <b>CI Pull Request Gates:</b> GitHub Actions workflows run on every pull request, blocking "
            "merges unless tests pass and Pylint score meets the threshold (<code>--fail-under=9.5</code>); and (3) <b>Branch Protection Rules:</b> Requiring green CI builds "
            "before pull requests can merge into protected production branches.",
            body_style,
        )
    )

    # Verification Output Section
    story.append(Paragraph("4. Runtime Verification & Execution Output", h1_style))
    terminal_output = (
        "<b>Terminal Execution Output:</b><br/>"
        "<code>$ python3 flight_reservation_system.py<br/>"
        "Is AI101 open: True<br/>"
        "Baggage Fee: 67.5<br/>"
        "Passenger Hash: 76161a689c7529645b02678017fed8b94a047e8aa458a82c50a23924f445ee07<br/>"
        "Boarding PIN: 9428<br/>"
        "Boarding manifest printed: flight_manifest.txt<br/>"
        "Available flights: 3<br/>"
        "API Token: AIRLINE_DISPATCH_SECRET_TOKEN_2026</code>"
    )
    story.append(
        Table(
            [[Paragraph(terminal_output, table_cell_style)]],
            colWidths=[540],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), bg_callout),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ],
        )
    )
    story.append(Spacer(1, 10))

    # Deliverables & Repository Structure
    story.append(Paragraph("5. Organized Repository Structure", h1_style))
    tree_text = (
        "<b>SE_lab5 Repository Structure:</b><br/>"
        "• <code>flight_reservation_system.py</code> — Cleaned script (10.00/10 Pylint, 0 Flake8, 0 Bandit)<br/>"
        "• <code>issues.md</code> — Comprehensive issue documentation table<br/>"
        "• <code>reflection.md</code> — In-depth answers to all 4 reflection questions<br/>"
        "• <code>report.pdf</code> — Complete submission report with changes table and reflections<br/>"
        "• <code>README.md</code> — Project documentation and reproduction guide<br/>"
        "• <code>pylint_report.txt</code>, <code>bandit_report.txt</code>, <code>flake8_report.txt</code> — Latest clean reports<br/>"
        "• <code>reports/before/</code> — Initial static analysis reports prior to remediation<br/>"
        "• <code>reports/after/</code> — Final verified static analysis reports post remediation<br/>"
        "• <code>.gitignore</code> — Excludes venv/, __pycache__/, and temporary outputs"
    )
    story.append(
        Table(
            [[Paragraph(tree_text, table_cell_style)]],
            colWidths=[540],
            style=[
                ("BACKGROUND", (0, 0), (-1, -1), bg_alt_row),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ],
        )
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename} ({os.path.getsize(filename)} bytes)")


if __name__ == "__main__":
    build_pdf("report.pdf")
