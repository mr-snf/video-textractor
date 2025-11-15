from fpdf import FPDF
import config
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Extracted Text from Video', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(text_content, filename=config.DEFAULT_PDF_FILENAME):
    """Generate a PDF file from the extracted text."""
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        
    output_path = os.path.join(config.OUTPUT_DIR, filename)
    
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(text_content)
    pdf.output(output_path)
    print(f"Successfully generated PDF: {output_path}")
