"""PDF metin çıkarma (PyMuPDF)."""
from __future__ import annotations

from extractors.text_cleaner import clean_text


def extract_text_from_pdf(file_path: str) -> str:
    """PDF dosyasından metin çıkarır. PyMuPDF yoksa boş döner."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return ""
    text_parts = []
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text_parts.append(page.get_text())
    except Exception as exc:  # noqa: BLE001
        return f""  # sessizce boş döner; çağıran taraf uyarır
    return clean_text("\n".join(text_parts))
