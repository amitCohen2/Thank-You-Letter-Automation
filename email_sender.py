import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailSender:
    def __init__(self, sender_email: str, sender_password: str, subject_text: str, body_text: str) -> None:
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.body_text = body_text
        self.subject_text = subject_text
        self.server = None  # SMTP server instance
        self.login()  # Login once on initialization

    def login(self) -> None:
        """Establish a persistent SMTP connection."""
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)  # ✅ Correct SMTP server
        self.server.login(self.sender_email, self.sender_password)
        print("Logged in to email server.")

    def send_email(self, to_email: str, pdf_attachment: str) -> None:
        """Send an email using the existing SMTP session."""
        if not self.server:
            raise Exception("SMTP session is not established. Call login() first.")

        # Convert the plain text body to an HTML email with right alignment
        html_body = """\
        <html>
            <body style="direction: rtl; text-align: right; font-family: Arial, sans-serif;">
                <p>{}</p>
            </body>
        </html>
        """.format(self.body_text.replace("\n", "<br>"))  # ✅ Properly formatted without f-string

        # Setup MIME
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = self.subject_text

        # Attach the HTML content
        msg.attach(MIMEText(html_body, "html"))

        # Ensure the file has a .pdf extension
        filename = os.path.basename(pdf_attachment)
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        # Attach PDF
        with open(pdf_attachment, "rb") as attachment:
            part = MIMEBase("application", "pdf")  # Use "pdf" directly since it's a known MIME type
            part.set_payload(attachment.read())
            encoders.encode_base64(part)

            # Correct headers
            part.add_header("Content-Disposition", 'attachment', filename=filename)
            part.add_header("Content-Type", 'application/pdf')

            msg.attach(part)

            # Send email using the existing session
        self.server.sendmail(self.sender_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")

    def close(self) -> None:
        """Close the SMTP session when done."""
        if self.server:
            self.server.quit()
            self.server = None
            print("SMTP session closed.")

