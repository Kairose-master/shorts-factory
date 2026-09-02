"""Print each guide to A4. Chromium is what rendered the page in the first
place, so the PDF is the same layout rather than a re-typeset approximation."""
import os, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
# The built pages live outside the repo; point this at wherever they are.
SRC = Path(os.environ.get("GUIDE_SRC", HERE.parent / "docs" / "_build"))
JOBS = [
    ("guide-mac.html",       "쇼츠-만들기-맥.pdf",       "쇼츠 만들기 · 맥"),
    ("guide-win.html",       "쇼츠-만들기-윈도우.pdf",   "쇼츠 만들기 · 윈도우"),
    ("guide-anychurch.html", "우리교회-쇼츠-만들기.pdf", "우리 교회 설교 쇼츠 만들기"),
]

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                            args=["--no-sandbox"])
    for src, out, title in JOBS:
        page = b.new_page()
        # A full HTML document, so the head/link tags are honoured.
        html = (SRC / src).read_text(encoding="utf-8")
        page.set_content(f"<!doctype html><html lang=ko><head><meta charset=utf-8>{html}",
                         wait_until="networkidle")
        try:
            page.wait_for_function("document.fonts.ready.then(()=>true)", timeout=20000)
        except Exception:
            print(f"  {src}: 폰트 대기 실패 — 그대로 진행")
        time.sleep(1.0)
        page.pdf(path=str(HERE.parent / "docs" / "pdf" / out), format="A4",
                 print_background=True,
                 margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"},
                 display_header_footer=True,
                 header_template="<div></div>",
                 footer_template=(
                     '<div style="width:100%;font-size:8pt;color:#8C8474;'
                     'font-family:sans-serif;padding:0 14mm;display:flex;'
                     'justify-content:space-between">'
                     f'<span>{title}</span>'
                     '<span class="pageNumber"></span></div>'))
        page.close()
        print(f"  wrote docs/pdf/{out}")
    b.close()
