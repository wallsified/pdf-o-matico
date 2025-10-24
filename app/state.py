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
    language: str = "en"

    @rx.var
    def back_to_tools_text(self) -> str:
        return "Back to Tools" if self.language == "en" else "Cambiar de Herramienta"

    @rx.var
    def subtitle_text(self) -> str:
        return (
            "Quick tools for PDF manipulation."
            if self.language == "en"
            else "Herramientas rápidas para manipulación de PDFs."
        )

    @rx.var
    def tools(self) -> list[Tool]:
        """Get the list of tools based on the current language."""
        if self.language == "es":
            return [
                {
                    "icon": "file-symlink",
                    "title": "Dividir PDF",
                    "description": "Separar un PDF en múltiples archivos por rango de páginas",
                    "url": "/split-pdf",
                },
                {
                    "icon": "merge",
                    "title": "Unir PDF",
                    "description": "Combinar múltiples PDFs en un solo documento",
                    "url": "/merge-pdf",
                },
                {
                    "icon": "archive",
                    "title": "Comprimir PDF",
                    "description": "Reducir el tamaño del archivo manteniendo la calidad",
                    "url": "/compress-pdf",
                },
                {
                    "icon": "image",
                    "title": "PDF a Imágenes",
                    "description": "Exportar todas las páginas como imágenes en un archivo ZIP",
                    "url": "/pdf-to-images",
                },
                {
                    "icon": "file-output",
                    "title": "Extraer Páginas",
                    "description": "Seleccionar y extraer páginas específicas de su PDF",
                    "url": "/extract-pages",
                },
                {
                    "icon": "rotate-cw",
                    "title": "Rotar Páginas",
                    "description": "Rotar páginas en sentido horario o antihorario",
                    "url": "/rotate-pages",
                },
            ]
        return [
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
                "icon": "archive",
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

    @rx.event
    def toggle_language(self):
        """Toggle the language between English and Spanish."""
        self.language = "es" if self.language == "en" else "en"