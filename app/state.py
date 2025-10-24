import reflex as rx
from typing import TypedDict


class Tool(TypedDict):
    """A dictionary representing a PDF tool."""

    icon: str
    title: str
    description: str
    url: str


class State(rx.State):
    """The main application state."""

    is_dark: bool = True
    tools: list[Tool] = [
        {
            "icon": "file-symlink",
            "title": "Split PDF",
            "description": "Separate a PDF into multiple files by page range",
            "url": "/split-pdf",
        },
        {
            "icon": "merge",
            "title": "Merge PDF",
            "description": "Combine multiple PDFs into a single document",
            "url": "/merge-pdf",
        },
        {
            "icon": "compress",
            "title": "Compress PDF",
            "description": "Reduce file size while maintaining quality",
            "url": "/compress-pdf",
        },
        {
            "icon": "image",
            "title": "PDF to Images",
            "description": "Export all pages as images in a ZIP file",
            "url": "/pdf-to-images",
        },
        {
            "icon": "file-output",
            "title": "Extract Pages",
            "description": "Select and extract specific pages from your PDF",
            "url": "/extract-pages",
        },
        {
            "icon": "rotate-cw",
            "title": "Rotate Pages",
            "description": "Rotate pages clockwise or counterclockwise",
            "url": "/rotate-pages",
        },
    ]

    @rx.event
    def toggle_theme(self):
        """Toggle the theme between light and dark mode."""
        self.is_dark = not self.is_dark