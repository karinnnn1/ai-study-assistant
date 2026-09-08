from pypdf import PdfReader


def get_pdf_page_count(pdf_file) -> int:
    """Return the number of pages in a PDF."""
    reader = PdfReader(pdf_file)

    return len(reader.pages)