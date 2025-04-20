from config import Config
from email_sender import EmailSender
from pdf_editor import PDFEditor
from program import Program


class App:
    """Handles initialization and application startup."""

    @staticmethod
    def start():
        email_sender = EmailSender(
            Config.EMAIL_SENDER_ADDRESS,
            Config.EMAIL_SENDER_PASSWORD,
            Config.MAIL_SUBJECT,
            Config.MAIL_BODY
        )

        pdf_editor = PDFEditor(
            Config.FONT_REGULAR, Config.FONT_SIZE_REGULAR,
            Config.FONT_BOLD, Config.FONT_SIZE_BOLD,
            Config.FONT_REGULAR_PATH, Config.FONT_BOLD_PATH
        )

        program = Program(pdf_editor, email_sender, Config)
        program.run()


if __name__ == '__main__':
    App.start()
