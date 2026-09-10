from pypdf import PdfReader


def get_pdf_page_count(pdf_file) -> int:
    """Return the number of pages in a PDF."""
    pdf_file.seek(0)
    reader = PdfReader(pdf_file)

    return len(reader.pages)


def extract_pdf_text(pdf_file) -> str:
    """Extract text from all pages of a PDF."""
    pdf_file.seek(0)
    reader = PdfReader(pdf_file)

    page_texts = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            page_texts.append(text)

    return "\n".join(page_texts)