"""State for the Rotate Pages tool page."""

import reflex as rx
from .base_state import PDFToolState
import pypdf
import io
import os
import logging


class RotatePagesState(rx.State, PDFToolState):
    """State to handle rotating pages in a PDF."""

    is_dark: bool = True
    is_processing: bool = False
    error_message: str = ""
    uploaded_file: str = ""
    rotation_angle: int = 90
    processed: bool = False

    @rx.event
    def set_rotation_angle(self, angle: str):
        """Set the rotation angle from the select component."""
        self.rotation_angle = int(angle)

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a single PDF file for rotation."""
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
    def rotate_pdf(self):
        """Rotate all pages of the PDF by the selected angle."""
        self.is_processing = True
        self.error_message = ""
        self.processed = False
        if not self.uploaded_file:
            self.error_message = "Please upload a PDF file first."
            self.is_processing = False
            return
        if self.rotation_angle not in [90, 180, 270]:
            self.error_message = (
                "Invalid rotation angle. Please select 90, 180, or 270 degrees."
            )
            self.is_processing = False
            return
        try:
            input_path = rx.get_upload_dir() / self.uploaded_file
            reader = pypdf.PdfReader(input_path)
            writer = pypdf.PdfWriter()
            for page in reader.pages:
                page.rotate(self.rotation_angle)
                writer.add_page(page)
            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)
            base_name = os.path.splitext(self.uploaded_file)[0]
            self.processed = True
            self.is_processing = False
            return rx.download(
                data=output_buffer.getvalue(), filename=f"{base_name}_rotated.pdf"
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = f"An error occurred during rotation: {e}"
        finally:
            self.is_processing = False
            if self.uploaded_file:
                try:
                    os.remove(rx.get_upload_dir() / self.uploaded_file)
                    self.uploaded_file = ""
                except OSError as e:
                    logging.exception(f"Error: {e}")