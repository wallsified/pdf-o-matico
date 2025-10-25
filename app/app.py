import reflex as rx
from app.pages import (
    index,
    split_pdf_page,
    merge_pdf_page,
    compress_pdf_page,
    pdf_to_images_page,
    extract_pages_page,
    rotate_pages_page,
)

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900&display=swap"
    ],
)
app.add_page(index, route="/")
app.add_page(split_pdf_page, route="/split-pdf")
app.add_page(merge_pdf_page, route="/merge-pdf")
app.add_page(compress_pdf_page, route="/compress-pdf")
app.add_page(pdf_to_images_page, route="/pdf-to-images")
app.add_page(extract_pages_page, route="/extract-pages")
app.add_page(rotate_pages_page, route="/rotate-pages")