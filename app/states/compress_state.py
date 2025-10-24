"""State for the Compress PDF tool page."""

import reflex as rx
from .base_state import PDFToolState
import pypdf
import io
import os
import logging


class CompressState(rx.State, PDFToolState):
    """State to handle compressing a PDF file."""

    is_dark: bool = True
    is_processing: bool = False
    error_message: str = ""
    uploaded_file: str = ""
    processed: bool = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a single PDF file for compression."""
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
        output_path = rx.get_upload_dir() / file.name
        with open(output_path, "wb") as f:
            f.write(upload_data)
        self.uploaded_file = file.name
        self.is_processing = False

    @rx.event
    def compress_pdf(self):
        """Compress the uploaded PDF file."""
        self.is_processing = True
        self.error_message = ""
        self.processed = False
        if not self.uploaded_file:
            self.error_message = "Please upload a PDF file first."
            self.is_processing = False
            return
        try:
            input_path = rx.get_upload_dir() / self.uploaded_file
            reader = pypdf.PdfReader(input_path)
            writer = pypdf.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            for page in writer.pages:
                page.compress_content_streams()
            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)
            base_name = os.path.splitext(self.uploaded_file)[0]
            self.processed = True
            self.is_processing = False
            return rx.download(
                data=output_buffer.getvalue(), filename=f"{base_name}_compressed.pdf"
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = f"An error occurred during compression: {e}"
        finally:
            self.is_processing = False
            if self.uploaded_file:
                try:
                    os.remove(rx.get_upload_dir() / self.uploaded_file)
                    self.uploaded_file = ""
                except OSError as e:
                    logging.exception(f"Error: {e}")