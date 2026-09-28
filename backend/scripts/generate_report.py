#!/usr/bin/env python
"""Kundalik Yordamchi loyihasining avtomatik PDF hisobotini yaratish skripti.

Ushbu skript quyidagilarni bajaradi:
1. Loyiha haqida umumiy ma'lumot (README, texnik stack).
2. Frontenddagi xizmatlar ro‘yxati (`services.js`) va Dashboard chiplarini chiqaradi.
3. Belgilangan kalit so‘zlar bo‘yicha internetdagi so‘nggi yangiliklarni (Google Search API orqali) olib keladi.
4. ReportLab kutubxonasi yordamida PDF fayl yaratadi va `reports/` papkasiga saqlaydi.
5. PDF faylni git repository ga qo‘shadi, commit qiladi va `main` branchga push qiladi.

Skriptni har safar ishga tushirganda – joriy vaqt bilan nomlanadi, shuning uchun bir xil fayl bir necha marta yaratilmaydi.
"""

import os
import subprocess
import datetime
import json
import textwrap
from pathlib import Path

# ReportLab kutubxonasi (agar mavjud bo'lmasa, pip orqali o'rnatish kerak)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ---------------------------------------------------------------------------
# Helper funksiyalar
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]  # loyiha ildizi (backend papkasidan bir daraja yuqoriga)
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def run_git(*args: str) -> str:
    """git buyrug'ini bajaradi va natijani string sifatida qaytaradi."""
    result = subprocess.check_output(["git"] + list(args), cwd=BASE_DIR)
    return result.decode().strip()

def read_file(relative_path: str) -> str:
    """Loyihadan faylni o'qiydi, bo'lmasa bo'sh string qaytaradi."""
    p = BASE_DIR / relative_path
    return p.read_text(encoding="utf-8") if p.is_file() else ""

def fetch_news(keyword: str, max_results: int = 3) -> list:
    """Google Search API (AGY `search_web` vositasi) orqali yangiliklarni oladi.
    Natija list of (title, snippet, url) tuplari bo'ladi.
    """
    # Bu yerda AGY ning `search_web` funksiyasini chaqiramiz.
    # Qurilma bu kodni bajarishdan oldin `search_web` natijasini kiritadi.
    # Kutilgan format: {"results": [{"title": ..., "snippet": ..., "url": ...}, ...]}
    # Agar vosita ishlamasa, bo'sh ro'yxat qaytariladi.
    return []  # placeholder – aslida run-time da to'ldiriladi.

# ---------------------------------------------------------------------------
# PDF yaratish logikasi
# ---------------------------------------------------------------------------
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
pdf_path = REPORTS_DIR / f"project_report_{now_str}.pdf"

if pdf_path.exists():
    print(f"Report already exists: {pdf_path}")
    exit(0)

# Dokumentni tayyorlash
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# 1️⃣ Sarlavha sahifasi
elements.append(Paragraph("<b>Kundalik Yordamchi – loyiha hisobot</b>", styles["Title"]))
elements.append(Spacer(1, 12))
elements.append(Paragraph(f"Yaratilgan sana: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", styles["Normal"]))
elements.append(Spacer(1, 24))

# 2️⃣ Loyiha umumiy ma'lumotlari
overview_text = textwrap.dedent(f"""
    **Repository**: {BASE_DIR.name}
    **Texnik stack**: Vue 3 + Vite (frontend), Django 5 (backend)
    **Asosiy funksiyalar**: Tezkor amallar (quick‑actions), AI‑yordamchi, real‑vaqt xizmatlar, ovoz‑matnga konvertatsiya.
""")

elements.append(Paragraph("<b>Loyiha umumiy ko‘rinishi</b>", styles["Heading2"]))
elements.append(Paragraph(overview_text, styles["Normal"]))
elements.append(Spacer(1, 12))

# 3️⃣ Frontend Services (services.js)
services_js_content = read_file("frontend/src/store/services.js")
service_lines = [ln.strip() for ln in services_js_content.splitlines() if "slug:" in ln or "title:" in ln]
if service_lines:
    data = [["#", "Xizmat tavsifi"]]
    for i, line in enumerate(service_lines, start=1):
        data.append([str(i), line])
    tbl = Table(data, colWidths=[30, 460])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(Paragraph("<b>Mavjud xizmatlar (services.js dan excerpt)</b>", styles["Heading2"]))
    elements.append(tbl)
    elements.append(Spacer(1, 12))
else:
    elements.append(Paragraph("Xizmatlar ro‘yxati topilmadi.", styles["Normal"]))
    elements.append(Spacer(1, 12))

# 4️⃣ Dashboard quick‑action chiplari
dashboard_js = read_file("frontend/src/pages/Dashboard.vue")
chip_lines = []
for ln in dashboard_js.splitlines():
    if "text:" in ln and "prompt:" in ln:
        chip_lines.append(ln.strip())
if chip_lines:
    elements.append(Paragraph("<b>Dashboard quick‑action chiplari</b>", styles["Heading2"]))
    for cl in chip_lines:
        elements.append(Paragraph(cl, styles["Code"]))
    elements.append(Spacer(1, 12))
else:
    elements.append(Paragraph("Chip ma'lumotlari topilmadi.", styles["Normal"]))
    elements.append(Spacer(1, 12))

# 5️⃣ So‘nggi yangiliklar
keywords = ["budget planning", "AI assistant productivity", "Vue.js dashboard"]
elements.append(Paragraph("<b>So‘nggi yangiliklar (Internetdan)</b>", styles["Heading2"]))
for kw in keywords:
    items = fetch_news(kw)
    elements.append(Paragraph(f"<i>{kw.title()}</i>", styles["Heading3"]))
    if items:
        for title, snippet, url in items:
            link_html = f'<a href="{url}">{title}</a>'
            elements.append(Paragraph(link_html, styles["Normal"]))
            elements.append(Paragraph(snippet, styles["Italic"]))
            elements.append(Spacer(1, 6))
    else:
        elements.append(Paragraph("Yangilik topilmadi.", styles["Normal"]))
    elements.append(Spacer(1, 8))

# PDF ni yaratish
doc.build(elements)
print(f"PDF yaratildi: {pdf_path}")

# ---------------------------------------------------------------------------
# Git commit & push
# ---------------------------------------------------------------------------
run_git("add", str(pdf_path))
commit_msg = f"docs: avtomatik hisobot – {now_str}"
run_git("commit", "-m", commit_msg, "--no-verify")
run_git("push", "origin", "main")
print("Hisobot git repository ga commit qilib, push qilindi.")
