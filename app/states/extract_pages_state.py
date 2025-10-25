"""State for the Extract Pages tool page."""

import reflex as rx
from .base_state import PDFToolState
import pypdf
import io
import os
import logging


class ExtractPagesState(rx.State, PDFToolState):
    """State to handle extracting pages from a PDF."""

    is_dark: bool = True
    is_processing: bool = False
    error_message: str = ""
    uploaded_file: str = ""
    page_selection: str = ""
    total_pages: int = 0
    processed: bool = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a single PDF file for page extraction."""
        self.is_processing = True
        self.error_message = ""
        self.uploaded_file = ""
        self.processed = False
        if not files:
            self.error_message = "No file was selected."
            self.is_processing = False
            return
        file = files[0]
        upload_data = await file.read()
        if not self._validate_pdf(upload_data):
            self.is_processing = False
            return
        pdf = pypdf.PdfReader(io.BytesIO(upload_data))
        self.total_pages = len(pdf.pages)
        output_path = rx.get_upload_dir() / file.name
        with open(output_path, "wb") as f:
            f.write(upload_data)
        self.uploaded_file = file.name
        self.is_processing = False

    @rx.event
    def extract_pages(self):
        """Extract selected pages from the PDF."""
        self.is_processing = True
        self.error_message = ""
        self.processed = False
        if not self.uploaded_file:
            self.error_message = "Please upload a PDF file first."
            self.is_processing = False
            return
        if not self.page_selection:
            self.error_message = "Please enter pages or ranges to extract."
            self.is_processing = False
            return
        try:
            input_path = rx.get_upload_dir() / self.uploaded_file
            reader = pypdf.PdfReader(input_path)
            writer = pypdf.PdfWriter()
            pages_to_extract = self._parse_page_range(
                self.page_selection, self.total_pages
            )
            if pages_to_extract is None:
                self.error_message = f"Invalid page selection: '{self.page_selection}'. Use comma-separated numbers or ranges (e.g., 1,3-5)."
                self.is_processing = False
                return
            for page_num in pages_to_extract:
                writer.add_page(reader.pages[page_num - 1])
            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)
            base_name = os.path.splitext(self.uploaded_file)[0]
            self.processed = True
            self.is_processing = False
            return rx.download(
                data=output_buffer.getvalue(), filename=f"{base_name}_extracted.pdf"
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = f"An error occurred during page extraction: {e}"
        finally:
            self.is_processing = False
            if self.uploaded_file:
                try:
                    os.remove(rx.get_upload_dir() / self.uploaded_file)
                    self.uploaded_file = ""
                except OSError as e:
                    logging.exception(f"Error: {e}")

    def _parse_page_range(self, range_str: str, total_pages: int) -> list[int] | None:
        pages = set()
        try:
            parts = range_str.split(",")
            for part in parts:
                part = part.strip()
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    if start > end or start < 1 or end > total_pages:
                        return None
                    pages.update(range(start, end + 1))
                else:
                    page = int(part)
                    if page < 1 or page > total_pages:
                        return None
                    pages.add(page)
            return sorted(list(pages))
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return None