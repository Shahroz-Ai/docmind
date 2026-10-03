import pymupdf


def load_pdf(file_path):
    """Extract text from each page of a PDF file."""
    doc = pymupdf.open(file_path)
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append({"page": page_num, "text": text})
    return pages


def load_pdf_bytes(data):
    """Extract text from each page of an uploaded PDF (bytes)."""
    doc = pymupdf.open(stream=data, filetype="pdf")
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append({"page": page_num, "text": text})
    return pages


def chunk_pages(pages, chunk_size=800, overlap=150):
    """Split each page's text into overlapping chunks."""
    chunks = []
    for p in pages:
        text = p["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append({"page": p["page"], "text": text[start:end]})
            start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    pages = load_pdf("sample.pdf")
    chunks = chunk_pages(pages)
    print(f"Total pages: {len(pages)}")
    print(f"Total chunks: {len(chunks)}")
    print("\nFirst chunk:\n", chunks[0])