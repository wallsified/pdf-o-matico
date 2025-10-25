"""State for the Merge PDF tool page."""

import reflex as rx
from .base_state import PDFToolState
import pypdf
import io
import os
import logging


class MergeState(rx.State, PDFToolState):
    """State to handle merging multiple PDF files."""

    is_dark: bool = True
    is_processing: bool = False
    error_message: str = ""
    uploaded_files: list[str] = []
    processed: bool = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of multiple PDF files for merging."""
        self.is_processing = True
        self.error_message = ""
        self.processed = False
        if not files:
            self.error_message = "No files were selected."
            self.is_processing = False
            return
        valid_files = []
        for file in files:
            upload_data = await file.read()
            if self._validate_pdf(upload_data):
                output_path = rx.get_upload_dir() / file.name
                with open(output_path, "wb") as f:
                    f.write(upload_data)
                valid_files.append(file.name)
            else:
                self.is_processing = False
                return
        self.uploaded_files.extend(valid_files)
        self.is_processing = False

    @rx.event
    def merge_pdfs(self):
        """Merge the uploaded PDF files into a single document."""
        self.is_processing = True
        self.error_message = ""
        self.processed = False
        if len(self.uploaded_files) < 2:
            self.error_message = "Please upload at least two PDF files to merge."
            self.is_processing = False
            return
        try:
            merger = pypdf.PdfMerger()
            for filename in self.uploaded_files:
                input_path = rx.get_upload_dir() / filename
                merger.append(input_path)
            output_buffer = io.BytesIO()
            merger.write(output_buffer)
            merger.close()
            output_buffer.seek(0)
            self.processed = True
            self.is_processing = False
            return rx.download(
                data=output_buffer.getvalue(), filename="merged_document.pdf"
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = f"An error occurred during merging: {e}"
        finally:
            self.is_processing = False
            for filename in self.uploaded_files:
                try:
                    os.remove(rx.get_upload_dir() / filename)
                except OSError as e:
                    logging.exception(f"Error: {e}")
            self.uploaded_files = []