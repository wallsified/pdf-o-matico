"""Base state for all PDF tool pages."""

import pypdf
import io
import logging


class PDFToolState:
    """A base state for all PDF tool pages, handling common logic."""

    def _validate_pdf(self, file_data: bytes) -> bool:
        """Validate if the uploaded file data is a valid PDF."""
        try:
            pdf = pypdf.PdfReader(io.BytesIO(file_data))
            if len(pdf.pages) > 0:
                return True
            self.error_message = "The provided PDF is empty or corrupted."
            return False
        except pypdf.errors.PdfReadError as e:
            logging.exception(f"Error: {e}")
            self.error_message = "Invalid file type. Please upload a valid PDF file."
            return False
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = f"An unexpected error occurred: {e}"
            return False