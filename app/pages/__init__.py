import reflex as rx


def index():
    return rx.el.div("Index Page")


def split_pdf_page():
    return rx.el.div("Split PDF Page")


def merge_pdf_page():
    return rx.el.div("Merge PDF Page")


def compress_pdf_page():
    return rx.el.div("Compress PDF Page")


def pdf_to_images_page():
    return rx.el.div("PDF to Images Page")


def extract_pages_page():
    return rx.el.div("Extract Pages Page")


def rotate_pages_page():
    return rx.el.div("Rotate Pages Page")