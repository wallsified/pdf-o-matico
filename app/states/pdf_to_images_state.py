"""State for the PDF to Images tool page."""

import reflex as rx
from .base_state import PDFToolState
from PIL import Image
import pymupdf as fitz
import zipfile
import io
import os
import logging


class PDFToImagesState(rx.State, PDFToolState):
    """State to handle converting PDF to images."""

    is_dark: bool = True
    is_processing: bool = False
    error_message: str = ""
    uploaded_file: str = ""
    processed: bool = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a single PDF file for conversion."""
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
    def convert_to_images(self):
        """Convert PDF pages to PNG images and package them in a ZIP file."""
        self.is_processing = True
        self.error_message = ""
        self.processed = False
        if not self.uploaded_file:
            self.error_message = "Please upload a PDF file first."
            self.is_processing = False
            return
        try:
            input_path = rx.get_upload_dir() / self.uploaded_file
            doc = fitz.open(stream=input_path.read_bytes(), filetype="pdf")
            zip_buffer = io.BytesIO()
            base_name = os.path.splitext(self.uploaded_file)[0]
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, page in enumerate(doc):
                    pix = page.get_pixmap()
                    img_buffer = io.BytesIO()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img.save(img_buffer, format="PNG")
                    img_buffer.seek(0)
                    zf.writestr(f"{base_name}_page_{i + 1}.png", img_buffer.getvalue())
            doc.close()
            zip_buffer.seek(0)
            self.processed = True
            self.is_processing = False
            return rx.download(
                data=zip_buffer.getvalue(), filename=f"{base_name}_images.zip"
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = f"An error occurred during image conversion: {e}"
        finally:
            self.is_processing = False
            if self.uploaded_file:
                try:
                    os.remove(rx.get_upload_dir() / self.uploaded_file)
                    self.uploaded_file = ""
                except OSError as e:
                    logging.exception(f"Error: {e}")
