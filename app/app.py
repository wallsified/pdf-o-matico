import reflex as rx
from .state import State
from .states.split_state import SplitState
from .states.merge_state import MergeState
from .states.compress_state import CompressState
from .states.pdf_to_images_state import PDFToImagesState
from .states.extract_pages_state import ExtractPagesState
from .states.rotate_pages_state import RotatePagesState


def tool_card(tool: dict) -> rx.Component:
    """
    Renders a single tool card with Material Design styling.

    Args:
        tool: A dictionary containing tool information (icon, title, description).

    Returns:
        A component representing the tool card.
    """
    return rx.el.a(
        rx.el.div(
            rx.icon(tool["icon"], class_name="h-10 w-10 mb-4 text-[#88C0D0]"),
            rx.el.h3(
                tool["title"],
                class_name=rx.cond(
                    State.is_dark,
                    "text-xl font-semibold text-[#ECEFF4]",
                    "text-xl font-semibold text-[#2E3440]",
                ),
            ),
            rx.el.p(
                tool["description"],
                class_name=rx.cond(
                    State.is_dark,
                    "text-sm text-[#D8DEE9] mt-2",
                    "text-sm text-[#4C566A] mt-2",
                ),
            ),
            class_name="p-6",
        ),
        href=tool["url"],
        class_name=rx.cond(
            State.is_dark,
            "bg-[#3B4252] rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 cursor-pointer",
            "bg-[#FFFFFF] rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 cursor-pointer",
        ),
    )


def header() -> rx.Component:
    """
    Renders the application header.

    Returns:
        A component representing the header.
    """
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "PDF-O-Matic",
                    class_name=rx.cond(
                        State.is_dark,
                        "text-2xl font-bold text-[#ECEFF4]",
                        "text-2xl font-bold text-[#2E3440]",
                    ),
                ),
                rx.el.h3(
                    State.subtitle_text,
                    class_name=rx.cond(
                        State.is_dark,
                        "text-sm font-bold text-[#ECEFF4]",
                        "text-sm font-bold text-[#2E3440]",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("globe", class_name="h-6 w-6"),
                    on_click=State.toggle_language,
                    class_name=rx.cond(
                        State.is_dark,
                        "p-2 rounded-full bg-[#4C566A] text-[#ECEFF4] hover:bg-[#5E81AC] transition-colors",
                        "p-2 rounded-full bg-[#E5E9F0] text-[#2E3440] hover:bg-[#D8DEE9] transition-colors",
                    ),
                ),
                rx.el.button(
                    rx.icon(
                        rx.cond(State.is_dark, "sun", "moon"), class_name="h-6 w-6"
                    ),
                    on_click=State.toggle_theme,
                    class_name=rx.cond(
                        State.is_dark,
                        "p-2 rounded-full bg-[#4C566A] text-[#ECEFF4] hover:bg-[#5E81AC] transition-colors",
                        "p-2 rounded-full bg-[#E5E9F0] text-[#2E3440] hover:bg-[#D8DEE9] transition-colors",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="container mx-auto flex justify-between items-center p-4",
        ),
        class_name=rx.cond(
            State.is_dark,
            "bg-[#2E3440] w-full",
            "bg-[#FFFFFF] w-full border-b border-[#E5E9F0]",
        ),
        style={"box-shadow": "0px 8px 16px rgba(0,0,0,0.2)"},
    )


def footer() -> rx.Component:
    """Renders the application footer."""
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.p(f"\t PDF-O-Matic 2025 - ", class_name="text-sm"),
                rx.el.div(
                    rx.el.a(
                        rx.icon("github", class_name="h-5 w-5"),
                        href="https://github.com/wallsified/pdf-o-matic",
                        target="_blank",
                        class_name=rx.cond(
                            State.is_dark,
                            "text-[#D8DEE9] hover:text-[#ECEFF4]",
                            "text-[#4C566A] hover:text-[#2E3440]",
                        ),
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="container mx-auto flex justify-between items-center p-4",
            ),
            class_name=rx.cond(
                State.is_dark, "border-t border-[#3B4252]", "border-t border-[#E5E9F0]"
            ),
        )
    )


@rx.page(route="/", title="PDF-O-Matic", description="PDF-O-Matic Home")
def index() -> rx.Component:
    """
    The main page of the application.

    Returns:
        A component representing the main page.
    """
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.foreach(State.tools, tool_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
                ),
                class_name="container mx-auto p-8",
            ),
            class_name="w-full h-full flex-1",
        ),
        footer(),
        class_name=rx.cond(
            State.is_dark,
            "min-h-screen flex flex-col font-['Red_Hat_Display'] bg-[#2E3440] text-[#D8DEE9]",
            "min-h-screen flex flex-col font-['Red_Hat_Display'] bg-[#ECEFF4] text-[#2E3440]",
        ),
    )


def tool_page_layout(title: str, *children) -> rx.Component:
    """A layout for all the tool pages."""
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                    State.back_to_tools_text,
                    href="/",
                    class_name=rx.cond(
                        State.is_dark,
                        "flex items-center text-sm text-[#D8DEE9] hover:text-[#ECEFF4] mb-6",
                        "flex items-center text-sm text-[#4C566A] hover:text-[#2E3440] mb-6",
                    ),
                ),
                rx.el.h2(
                    title,
                    class_name=rx.cond(
                        State.is_dark,
                        "text-3xl font-bold text-[#ECEFF4] mb-8",
                        "text-3xl font-bold text-[#2E3440] mb-8",
                    ),
                ),
                *children,
                class_name="container mx-auto p-8",
            ),
            class_name="flex-1",
        ),
        footer(),
        class_name=rx.cond(
            State.is_dark,
            "min-h-screen flex flex-col font-['Red_Hat_Display'] bg-[#2E3440] text-[#D8DEE9]",
            "min-h-screen flex flex-col font-['Red_Hat_Display'] bg-[#ECEFF4] text-[#2E3440]",
        ),
    )


def file_upload_component(
    state: rx.State, handler: rx.event.EventType, multiple: bool, upload_id: str
) -> rx.Component:
    """A reusable file upload component."""
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon(tag="cloud-upload", class_name="w-12 h-12 mb-4 text-[#88C0D0]"),
                rx.el.p(
                    rx.cond(
                        State.language == "en",
                        "Drag & drop files here, or click to select",
                        "Arrastra y suelta archivos aquí, o haz clic para seleccionar",
                    ),
                    class_name=rx.cond(
                        State.is_dark, "text-[#D8DEE9]", "text-[#4C566A]"
                    ),
                ),
                rx.el.span(
                    rx.cond(
                        State.language == "en", "PDF files only", "Solo archivos PDF"
                    ),
                    class_name=rx.cond(
                        State.is_dark,
                        "text-sm text-[#A3B2CC]",
                        "text-sm text-[#6B7280]",
                    ),
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg cursor-pointer transition-colors",
                border_color=rx.cond(State.is_dark, "#4C566A", "#D1D5DB"),
                _hover={"border_color": "#88C0D0"},
            ),
            id=upload_id,
            accept={"application/pdf": [".pdf"]},
            multiple=multiple,
            max_files=rx.cond(multiple, 50, 1),
            class_name="w-full",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files(upload_id),
                lambda file: rx.el.div(
                    rx.el.p(file, class_name="text-sm"),
                    class_name=rx.cond(
                        State.is_dark,
                        "p-2 bg-[#434C5E] rounded-md",
                        "p-2 bg-[#E5E9F0] rounded-md",
                    ),
                ),
            ),
            class_name="mt-4 space-y-2",
        ),
        rx.el.button(
            rx.cond(State.language == "en", "Upload", "Subir"),
            on_click=handler(rx.upload_files(upload_id=upload_id)),
            class_name="mt-4 w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
        ),
        rx.cond(
            state.error_message != "",
            rx.el.div(
                state.error_message,
                class_name="mt-4 p-2 text-sm text-white bg-[#BF616A] rounded-md",
            ),
        ),
        rx.cond(
            state.is_processing,
            rx.el.div(
                rx.spinner(),
                rx.el.p(
                    rx.cond(State.language == "en", "Processing...", "Procesando...")
                ),
                class_name="flex items-center gap-2 mt-4",
            ),
        ),
        class_name="w-full max-w-lg mx-auto",
    )


def processed_message(state: rx.State) -> rx.Component:
    return rx.cond(
        state.processed,
        rx.el.div(
            rx.icon(tag="square_check", class_name="w-5 h-5 text-green-500 mr-2"),
            rx.el.p(
                rx.cond(
                    State.language == "en",
                    "Processing complete! Your download will begin shortly.",
                    "¡Proceso completado! Tu descarga comenzará en breve.",
                )
            ),
            class_name="flex items-center mt-4 p-2 text-sm text-white bg-green-500/20 rounded-md border border-green-500",
        ),
    )


@rx.page(route="/split-pdf", title="Split PDF", description="PDF-o-Matic Split Tool")
def split_pdf() -> rx.Component:
    return tool_page_layout(
        rx.cond(State.language == "en", "Split PDF", "Dividir PDF"),
        file_upload_component(
            SplitState, SplitState.handle_upload, False, "split_upload"
        ),
        rx.cond(
            SplitState.uploaded_file != "",
            rx.el.div(
                rx.el.p(
                    rx.cond(
                        State.language == "en",
                        f"Total pages: {SplitState.total_pages}",
                        f"Páginas totales: {SplitState.total_pages}",
                    ),
                    class_name=rx.cond(
                        State.is_dark,
                        "text-sm text-[#D8DEE9] mb-2",
                        "text-sm text-[#4C566A] mb-2",
                    ),
                ),
                rx.el.input(
                    placeholder=rx.cond(
                        State.language == "en",
                        "Enter page ranges (e.g., 1-3, 5, 7-9)",
                        "Introduce rangos de páginas (ej: 1-3, 5, 7-9)",
                    ),
                    on_change=SplitState.set_split_ranges,
                    class_name="w-full p-2 border rounded-md bg-transparent mb-4",
                    border_color=rx.cond(State.is_dark, "#4C566A", "#D1D5DB"),
                    default_value=SplitState.split_ranges,
                ),
                rx.el.button(
                    rx.cond(
                        State.language == "en",
                        "Split PDF & Download",
                        "Dividir PDF y Descargar",
                    ),
                    on_click=SplitState.split_pdf,
                    class_name="w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
                ),
                processed_message(SplitState),
                class_name="mt-6 w-full max-w-lg mx-auto",
            ),
        ),
    )


@rx.page(route="/merge-pdf", title="Merge PDF", description="PDF-o-Matic Merge Tool")
def merge_pdf() -> rx.Component:
    return tool_page_layout(
        rx.cond(State.language == "en", "Merge PDF", "Unir PDF"),
        file_upload_component(
            MergeState, MergeState.handle_upload, True, "merge_upload"
        ),
        rx.cond(
            MergeState.uploaded_files.length() > 0,
            rx.el.div(
                rx.el.p(
                    rx.cond(
                        State.language == "en",
                        f"{MergeState.uploaded_files.length()} files selected.",
                        f"{MergeState.uploaded_files.length()} archivos seleccionados.",
                    ),
                    class_name=rx.cond(
                        State.is_dark,
                        "text-sm text-[#D8DEE9] mb-4",
                        "text-sm text-[#4C566A] mb-4",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        State.language == "en",
                        "Merge PDFs & Download",
                        "Unir PDFs y Descargar",
                    ),
                    on_click=MergeState.merge_pdfs,
                    class_name="w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
                ),
                processed_message(MergeState),
                class_name="mt-6 w-full max-w-lg mx-auto",
            ),
        ),
    )


@rx.page(
    route="/compress-pdf", title="Compress PDF", description="PDF-o-Matic Compress Tool"
)
def compress_pdf() -> rx.Component:
    return tool_page_layout(
        rx.cond(State.language == "en", "Compress PDF", "Comprimir PDF"),
        file_upload_component(
            CompressState, CompressState.handle_upload, False, "compress_upload"
        ),
        rx.cond(
            CompressState.uploaded_file != "",
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        State.language == "en",
                        "Compress PDF & Download",
                        "Comprimir PDF y Descargar",
                    ),
                    on_click=CompressState.compress_pdf,
                    class_name="w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
                ),
                processed_message(CompressState),
                class_name="mt-6 w-full max-w-lg mx-auto",
            ),
        ),
    )


def pdf_to_images() -> rx.Component:
    return tool_page_layout(
        rx.cond(State.language == "en", "PDF to Images", "PDF a Imágenes"),
        file_upload_component(
            PDFToImagesState,
            PDFToImagesState.handle_upload,
            False,
            "pdf_to_images_upload",
        ),
        rx.cond(
            PDFToImagesState.uploaded_file != "",
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        State.language == "en",
                        "Convert to Images & Download ZIP",
                        "Convertir a Imágenes y Descargar ZIP",
                    ),
                    on_click=PDFToImagesState.convert_to_images,
                    class_name="w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
                ),
                processed_message(PDFToImagesState),
                class_name="mt-6 w-full max-w-lg mx-auto",
            ),
        ),
    )


@rx.page(
    route="/extract-pages",
    title="Extract Pages",
    description="PDF-o-Matic Image Extractor",
)
def extract_pages() -> rx.Component:
    return tool_page_layout(
        rx.cond(State.language == "en", "Extract Pages", "Extraer Páginas"),
        file_upload_component(
            ExtractPagesState,
            ExtractPagesState.handle_upload,
            False,
            "extract_pages_upload",
        ),
        rx.cond(
            ExtractPagesState.uploaded_file != "",
            rx.el.div(
                rx.el.p(
                    rx.cond(
                        State.language == "en",
                        f"Total pages: {ExtractPagesState.total_pages}",
                        f"Páginas totales: {ExtractPagesState.total_pages}",
                    ),
                    class_name=rx.cond(
                        State.is_dark,
                        "text-sm text-[#D8DEE9] mb-2",
                        "text-sm text-[#4C566A] mb-2",
                    ),
                ),
                rx.el.input(
                    placeholder=rx.cond(
                        State.language == "en",
                        "Enter pages to extract (e.g., 1,3-5)",
                        "Introduce páginas a extraer (ej: 1,3-5)",
                    ),
                    on_change=ExtractPagesState.set_page_selection,
                    class_name="w-full p-2 border rounded-md bg-transparent mb-4",
                    border_color=rx.cond(State.is_dark, "#4C566A", "#D1D5DB"),
                    default_value=ExtractPagesState.page_selection,
                ),
                rx.el.button(
                    rx.cond(
                        State.language == "en",
                        "Extract Pages & Download",
                        "Extraer Páginas y Descargar",
                    ),
                    on_click=ExtractPagesState.extract_pages,
                    class_name="w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
                ),
                processed_message(ExtractPagesState),
                class_name="mt-6 w-full max-w-lg mx-auto",
            ),
        ),
    )


@rx.page(
    route="/rotate-pages", title="Rotate Pages", description="PDF-o-Matic Page Rotator"
)
def rotate_pages() -> rx.Component:
    return tool_page_layout(
        rx.cond(State.language == "en", "Rotate Pages", "Rotar Páginas"),
        file_upload_component(
            RotatePagesState,
            RotatePagesState.handle_upload,
            False,
            "rotate_pages_upload",
        ),
        rx.cond(
            RotatePagesState.uploaded_file != "",
            rx.el.div(
                rx.el.select(
                    rx.el.option(
                        rx.cond(
                            State.language == "en",
                            "90 degrees clockwise",
                            "90 grados en sentido horario",
                        ),
                        value="90",
                    ),
                    rx.el.option(
                        rx.cond(State.language == "en", "180 degrees", "180 grados"),
                        value="180",
                    ),
                    rx.el.option(
                        rx.cond(
                            State.language == "en",
                            "270 degrees clockwise",
                            "270 grados en sentido horario",
                        ),
                        value="270",
                    ),
                    default_value=RotatePagesState.rotation_angle.to_string(),
                    on_change=RotatePagesState.set_rotation_angle,
                    class_name="w-full p-2 border rounded-md bg-transparent mb-4",
                    _hover={"border_color": "#88C0D0"},
                    border_color=rx.cond(State.is_dark, "#4C566A", "#D1D5DB"),
                ),
                rx.el.button(
                    rx.cond(
                        State.language == "en",
                        "Rotate PDF & Download",
                        "Rotar PDF y Descargar",
                    ),
                    on_click=RotatePagesState.rotate_pdf,
                    class_name="w-full py-2 px-4 rounded-md text-white bg-[#5E81AC] hover:bg-[#81A1C1] transition-colors",
                ),
                processed_message(RotatePagesState),
                class_name="mt-6 w-full max-w-lg mx-auto",
            ),
        ),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900&display=swap"
    ],
)
