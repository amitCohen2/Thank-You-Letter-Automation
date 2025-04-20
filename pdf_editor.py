import os
import tempfile
from typing import Dict
import unicodedata
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF


class PDFEditor:
    def __init__(self, letter_font: str, letter_font_size: int, header_font: str,
                 header_font_size: int, letter_font_path: str, header_font_path: str) -> None:
        self.letter_font = letter_font
        self.letter_font_size = letter_font_size
        self.header_font = header_font
        self.header_font_size = header_font_size
        self.letter_font_path = letter_font_path
        self.header_font_path = header_font_path

    def overlay_text_on_existing_pdf(self, input_pdf: str, output_pdf: str, output_dir: str,
                                     text_data: Dict[str, str]) -> None:
        reader = PdfReader(input_pdf)
        page = reader.pages[0]

        pdf = FPDF(orientation='L', format='A4')
        pdf.add_page()

        # Add header font
        pdf.add_font(self.header_font, '', self.header_font_path)
        pdf.set_font(self.header_font, size=self.header_font_size)
        pdf.set_text_color(49, 56, 131)

        page_width = pdf.w  # A4 width in points (≈ 595)
        margin = 21
        right_margin = page_width - margin

        y_position = 50

        # Employer and Company Text
        if text_data['employer_name']:
            employer_text = f"{self.reverse_text_if_needed(text_data['employer_name'] + ', ')} {self.reverse_text_if_needed('לכבוד')}"
        else:
            employer_text = f"{self.reverse_text_if_needed('לכבוד ')}"
        company_text = f"{self.reverse_text_if_needed(text_data['company_name'])}"
        combined_text = f",{company_text}{employer_text}"

        text_width = pdf.get_string_width(combined_text)
        x_position = right_margin - text_width  # Ensure text stays within page bounds
        pdf.text(x_position, y_position, combined_text)

        # Add letter font for additional content
        pdf.add_font(self.letter_font, '', self.letter_font_path)
        pdf.set_font(self.letter_font, size=self.letter_font_size)

        # Soldier Name
        y_position += 18
        soldier_text = f"{self.reverse_text_if_needed('והגיבוי שאתם מעניקים ל' + text_data['soldier_name'] + ', המשרת במילואים בחטיבת הנגב.')}"
        # soldier_text = f"{self.reverse_text_if_needed('והגיבוי שאתם מעניקים ל' + text_data['partner_name'] + ' בן/בת זוגו/ה של ' + text_data['soldier_name'] +', המשרת/ת במילואים בחטיבת הנגב.')}"

        text_width = pdf.get_string_width(soldier_text)
        x_position = right_margin - text_width  # Ensure text stays visible
        pdf.text(x_position, y_position, soldier_text)

        # Save Overlay PDF
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            overlay_pdf_path = tmpfile.name
            pdf.output(overlay_pdf_path)

        # Merge with Original PDF
        overlay_reader = PdfReader(overlay_pdf_path)
        original_page = page
        overlay_page = overlay_reader.pages[0]
        original_page.merge_page(overlay_page)

        writer = PdfWriter()
        writer.add_page(original_page)
        output_path = os.path.join(output_dir, output_pdf)

        with open(output_path, "wb") as output_file:
            writer.write(output_file)

    def reverse_text_if_needed(self, text: str) -> str:
        def is_hebrew(c):
            return unicodedata.name(c, '').startswith('HEBREW')

        # Check if text contains any Hebrew letters
        contains_hebrew = any(is_hebrew(c) for c in text)
        # Check if text contains only English letters or digits
        contains_english = all(c.isascii() and not is_hebrew(c) for c in text if c.strip())

        if contains_hebrew and not contains_english:
            return text[::-1]  # Reverse only Hebrew text
        return text


