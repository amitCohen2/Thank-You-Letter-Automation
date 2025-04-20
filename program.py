import csv
import re
from config import Config
from email_sender import EmailSender
from pdf_editor import PDFEditor


class Program:
    """Handles PDF generation and email sending."""

    def __init__(self, pdf_editor: PDFEditor, email_sender: EmailSender, config: Config) -> None:
        self.pdf_editor = pdf_editor
        self.email_sender = email_sender
        self.config = config

    def run(self) -> None:
        """Reads CSV data, generates PDFs, and sends emails."""

        with open(self.config.CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            i = 0
            for row in reader:
                i += 1
                if not self.is_valid_email(row['employer_mail']):
                    print(
                        f"{i}. Skipping {row['employer_name']} ({row['soldier_name']}): Invalid email {row['employer_mail']}")
                    continue

                text_to_overlay = {
                    'employer_name': row['employer_name'],
                    # 'partner_name': row['partner_name'],  # for partners thank you letters
                    'company_name': row['company_name'],
                    'soldier_name': row['soldier_name'],
                }

                # output_pdf = f"{row['employer_name']}_{row['partner_name']}_thank_you_letter.pdf"
                output_pdf = f"{row['employer_name']}_{row['soldier_name']}_thank_you_letter.pdf"
                # Replace invalid characters
                output_pdf = re.sub(r'[<>:"/\\|?*]', '_', output_pdf)
                output_dir = r'outputs/outputs4/'

                self.pdf_editor.overlay_text_on_existing_pdf(self.config.PDF_TEMPLATE_PATH, output_pdf, output_dir,
                                                             text_to_overlay)
                print(f"{i}. Generated PDF for {row['employer_name']} ({row['soldier_name']})")
                # print(f"{i}. Generated PDF for {row['employer_name']} ({row['partner_name']})")

                # send the email with the relevant data
                self.email_sender.send_email(row['employer_mail'], output_dir + output_pdf)

        self.email_sender.close()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validates email format."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None


