"""Build Cameron_DeBough_Resume.pdf (one page, US Letter).

Usage:
    python3 resume/build_resume.py

Writes the PDF to the repo root, where the site links to it.
Needs reportlab and the Carlito fonts (fonts-crosextra-carlito).
"""

from pathlib import Path

from reportlab.lib.colors import Color, black
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Cameron_DeBough_Resume.pdf"

FONT_DIR = Path("/usr/share/fonts/truetype/crosextra")
pdfmetrics.registerFont(TTFont("Carlito", str(FONT_DIR / "Carlito-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-Bold", str(FONT_DIR / "Carlito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-Italic", str(FONT_DIR / "Carlito-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Carlito-BoldItalic", str(FONT_DIR / "Carlito-BoldItalic.ttf")))
pdfmetrics.registerFontFamily(
    "Carlito", normal="Carlito", bold="Carlito-Bold",
    italic="Carlito-Italic", boldItalic="Carlito-BoldItalic",
)

LINK = "#1f4e9e"
SIZE = 9.2
LEAD = 10.85
MARGIN = 42

name_style = ParagraphStyle("name", fontName="Carlito-Bold", fontSize=20, leading=22, alignment=TA_CENTER)
contact_style = ParagraphStyle("contact", fontName="Carlito", fontSize=8.3, leading=10, alignment=TA_CENTER)
body = ParagraphStyle("body", fontName="Carlito", fontSize=SIZE, leading=LEAD)
italic = ParagraphStyle("italic", parent=body, fontName="Carlito-Italic")
right = ParagraphStyle("right", parent=body, alignment=2)
bullet = ParagraphStyle(
    "bullet", parent=body, leftIndent=9, bulletIndent=1,
    bulletFontName="Helvetica", bulletFontSize=10,
)


class SectionHeading(Flowable):
    """Letter-spaced caps heading with a rule underneath."""

    def __init__(self, text, width):
        super().__init__()
        self.text = text
        self.width = width
        self.height = 15

    def wrap(self, *_):
        return self.width, self.height

    def draw(self):
        c = self.canv
        t = c.beginText(0, 5.2)
        t.setFont("Carlito-Bold", 10.5)
        t.setCharSpace(1.8)
        t.textOut(self.text)
        c.drawText(t)
        c.setLineWidth(0.6)
        c.setStrokeColor(black)
        c.line(0, 0, self.width, 0)


def link(url, text):
    return f'<a href="{url}" color="{LINK}">{text}</a>'


def esc(s):
    return s.replace("&", "&amp;")


def entry_head(left, date=None):
    if date is None:
        return Paragraph(left, body)
    t = Table(
        [[Paragraph(left, body), Paragraph(f"<b>{date}</b>", right)]],
        colWidths=[None, 150],
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def bullets(items):
    return [Paragraph(esc(i), bullet, bulletText="•") for i in items]


def entry(title, org, date=None, note=None, items=()):
    left = f"<b>{esc(title)}</b>" + (f", {org}" if org else "")
    out = [Spacer(1, 4), entry_head(left, date)]
    if note:
        out.append(Paragraph(esc(note), italic))
    out += bullets(items)
    return out


def section(title, width):
    # Negative spacer cancels the 4pt gap each entry adds above itself.
    return [Spacer(1, 6.5), SectionHeading(title, width), Spacer(1, -2.2)]


def build():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=letter,
        # Frames pad 6pt on every side, so text runs from x=42 to x=570.
        leftMargin=MARGIN - 6, rightMargin=MARGIN - 6, topMargin=30, bottomMargin=24,
        title="Cameron DeBough Resume", author="Cameron DeBough",
    )
    W = doc.width
    s = []

    s.append(Paragraph("Cameron DeBough", name_style))
    s.append(Spacer(1, 1))
    s.append(Paragraph(
        " · ".join([
            "Tucson, AZ",
            "(520) 861-8697",
            link("mailto:cameron.debough@gmail.com", "cameron.debough@gmail.com"),
            link("https://www.linkedin.com/in/camerondebough", "linkedin.com/in/camerondebough"),
            link("https://github.com/CameronDeb", "github.com/CameronDeb"),
            link("https://camerondebough.com", "camerondebough.com"),
        ]),
        contact_style,
    ))

    # EDUCATION
    s += section("EDUCATION", W)
    s += [Spacer(1, 4), entry_head(
        "<b>University of Arizona</b>, B.S. Computer Science &amp; Artificial Intelligence, Minor in Mathematics",
        "Expected May 2029",
    )]
    s.append(Paragraph(
        "GPA: 3.87 · Dean's List with Distinction (Fall 2025) · Dean's List (Spring 2026) · 67 Credits Completed",
        body,
    ))
    s.append(Paragraph(
        "<b>Coursework:</b> Software Development, Discrete Mathematics for CS I-II, Analyzing Data, "
        "Web Programming, Calculus I-II, Linear Algebra",
        body,
    ))

    # EXPERIENCE
    s += section("EXPERIENCE", W)
    s += entry(
        "Software Engineering Intern", "SkillfullyAware / SAAQ", "October 2025 - Present",
        items=[
            "Own the production backend of an AI-powered leadership assessment platform used by executive peer "
            "organizations (EO, YPO): Python and FastAPI services on Supabase (PostgreSQL), live in production",
            "Built a streaming LLM analysis pipeline with multi-stage scoring and two-pass generation that eliminated "
            "timeouts and truncated output, plus automated DOCX report generation from the analysis results",
            "Implementing authentication, Stripe payments, and persistent user storage for MVP launch",
        ],
    )
    s += entry(
        "Founder & Engineer",
        "DeBough Systems (" + link("https://deboughsystems.com", "deboughsystems.com") + ")",
        "August 2026 - Present",
        items=[
            "Built and launched a cybersecurity service that helps small businesses with no IT staff find and fix "
            "the weak spots attackers target most, with every issue explained in plain English",
            "Wrote a read-only checkup program that scans each company computer in about 40 seconds (updates, "
            "antivirus, firewall, disk encryption) and turns the results into a ranked fix list, a weekly email "
            "report, and a printable report for cyber insurers",
            "Built a free domain scan that checks whether attackers could fake a company's email or impersonate it "
            "with look-alike websites; Next.js, TypeScript, Supabase/Postgres, and Stripe, with rate limiting and "
            "ownership checks to prevent misuse",
        ],
    )

    # RESEARCH EXPERIENCE
    s += section("RESEARCH EXPERIENCE", W)
    s += entry(
        "Undergraduate Research Assistant", "VSI Lab, University of Arizona ECE", "September 2025 - Present",
        note="Embodied AI & Accessibility · Advisor: Prof. Eungjoo Lee",
        items=[
            "Led a real-robot study of online Gaussian Splatting SLAM (MonoGS) on a TurtleBot 4 against offline "
            "structure-from-motion (COLMAP, GLOMAP + 3DGS); online mapping took 2.4 min vs. 4.0 min for the "
            "fastest offline pipeline, at 31.0 vs. 29.7 dB PSNR",
            "Built the ROS 2 pipeline end to end: rosbag2 recording, dataset conversion, SLAM/SfM runs, "
            "and ATE, PSNR, SSIM, LPIPS evaluation",
            "Found the OAK-D depth camera reads 11 to 13% long and corrected it with lidar, cutting SLAM "
            "tracking error from 7.4 to 1.2 cm",
            "Also building NVIDIA Isaac Sim environments, ROS 2 control of LeRobot SO-101 arms, and computer-vision "
            "pipelines for Meta Aria 2 smart glasses (hand tracking, gaze data) for ASL accessibility",
        ],
    )
    s += entry(
        "Research Software Engineer", "NewFOS Center, University of Arizona", "March 2026 - Present",
        note="New Frontiers of Sound, an NSF Science & Technology Center",
        items=[
            "Built Python automation pipelines for nonlinear acoustics experiments (hysteresis sweeps, harmonic SNR "
            "analysis, transfer-function extraction) used to model signal distortion in acoustic transducers",
            "Designed and validated an electrical impedance measurement rig with a full de-embedding pipeline that "
            "isolated a 42% cable-parasitic error in a previously reported measurement",
            "Developed MATLAB signal-analysis pipelines (SVD, dynamic mode decomposition) that produced "
            "publication-quality figures for experiments on a three-rod coupled acoustic waveguide",
        ],
    )

    # PRESENTATIONS & AWARDS
    s += section("PRESENTATIONS & AWARDS", W)
    s += [Spacer(1, 4), entry_head(
        "<b>Poster</b>, Bay Area Robotics Symposium (BARS 2026), UC Berkeley", "October 2026",
    )]
    s.append(Paragraph(
        "<i>Online Gaussian Splatting SLAM on a TurtleBot4: Real-Robot Evaluation Against Offline "
        "Structure-from-Motion.</i> C. DeBough, W. Koh, E. Lee",
        body,
    ))
    s += [Spacer(1, 4), entry_head(
        "<b>Undergraduate Research Travel Grant ($1,000)</b>, University of Arizona",
        "Fall 2026",
    )]

    # TECHNICAL PROJECTS
    s += section("TECHNICAL PROJECTS", W)
    s.append(Spacer(1, 4))
    for name, desc in [
        ("Thermal-Tracking Turret", "Raspberry Pi turret that tracks a heat source in real time "
                                    "(I2C thermal array, PWM servos, closed-loop control)"),
        ("APEX QUANT", "event-driven backtesting and paper-trading engine for micro futures with risk controls "
                       "and an Interactive Brokers layer"),
        ("Synapse Finance", "full-stack financial SaaS with 50+ active users (Flask, React, PostgreSQL, "
                            "JWT auth, CI/CD)"),
    ]:
        s.append(Paragraph(f"<b>{name}:</b> {desc}", bullet, bulletText="\u2022"))

    # TECHNICAL SKILLS
    s += section("TECHNICAL SKILLS", W)
    s.append(Spacer(1, 4))
    for k, v in [
        ("Languages", "Python, C++, Java, JavaScript/TypeScript, SQL, MATLAB, Bash, HTML/CSS"),
        ("Frameworks", "FastAPI, Flask, React, Next.js, Node.js, Tailwind CSS"),
        ("Robotics & Hardware", "ROS 2, SLAM, Gaussian Splatting, COLMAP, Isaac Sim, Raspberry Pi, I2C, "
                                "PWM servo control, VISA/SCPI"),
        ("AI & Data", "PyTorch, agentic AI (tool calling, RAG), LLM integration, computer vision, NumPy, SciPy, "
                      "Pandas, signal processing"),
        ("Tools & Databases", "Git, Docker, Linux, PostgreSQL, Supabase, Stripe, CI/CD"),
    ]:
        s.append(Paragraph(f"<b>{esc(k)}:</b> {v}", body))

    # LEADERSHIP & ACTIVITIES
    s += section("LEADERSHIP & ACTIVITIES", W)
    s += entry(
        "Coke Fellow", "The Coca-Cola Company, Introships Program (1 of 50 fellows nationwide)", "May - July 2026",
    )
    s += entry(
        "Founder & Owner", "Durian Car Detailing", "May 2023 - Present",
        items=["Built and run a car detailing business from scratch with 200+ jobs completed, handling pricing, "
               "marketing, and customer service"],
    )
    s.append(Paragraph(
        "<b>University of Arizona AI Club</b> · MLH Global Hack Week · 13+ GitHub projects", body,
    ))

    pages = []
    doc.build(s, onLaterPages=lambda c, d: pages.append(c.getPageNumber()))
    if pages:
        raise SystemExit(f"Resume ran over one page ({len(pages) + 1} pages). Trim content.")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
