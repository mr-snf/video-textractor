from fpdf import FPDF
import config
import os


class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, "Extracted Text from Video", 0, 1, "C")

    def chapter_title(self, title):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("DejaVu", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()


def generate_pdf(text_content, filename=config.DEFAULT_PDF_FILENAME):
    """Generate a PDF file from the extracted text."""
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

    output_path = os.path.join(config.OUTPUT_DIR, filename)

    pdf = PDF()
    try:
        font_path = os.path.join(os.path.dirname(__file__), "fonts")
        pdf.add_font("DejaVu", "", os.path.join(font_path, "DejaVuSans.ttf"), uni=True)
        pdf.add_font(
            "DejaVu", "B", os.path.join(font_path, "DejaVuSans-Bold.ttf"), uni=True
        )
    except RuntimeError as e:
        if "not found" in str(e):
            print(
                "Dejavu font not found. Please download it from https://dejavu-fonts.github.io/Download.html"
            )
            print(
                "And place DejaVuSans.ttf and DejaVuSans-Bold.ttf in a 'fonts' directory inside the 'src' directory."
            )
            return
        raise e

    pdf.add_page()
    pdf.chapter_body(text_content)
    pdf.output(output_path)
    print(f"Successfully generated PDF: {output_path}")
