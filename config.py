class Config:
    """Stores configuration constants."""

    PDF_TEMPLATE_PATH = 'thank_you_letter_template.pdf'
    CSV_FILE_PATH = r'csv_files/thank_you_letters_details4.csv'
    MAIL_SUBJECT = "אגרת הוקרה והערכה על תמיכתכם במשרתי המילואים בחטיבת הנגב"
    MAIL_BODY = """שלום רב,

מצ"ב אגרת הוקרה כאות תודה על תרומתכם החשובה להמשכיות שירות המילואים ולביטחון המדינה.
תודה על מחויבותכם ועל היותכם חלק בלתי נפרד מהמאמץ הלאומי.

בהערכה רבה,
אל"ם יוסי אליאס
מפקד חטיבת הנגב
    """
    MAIL_BODY_PARTNERS = """שלום רב,

מצורפת בזאת אגרת הוקרה כאות תודה על תמיכתכם בעובדיכם, בני ובנות זוגם של משרתי המילואים בחטיבת הנגב.

התגייסותכם לטובת עובדיכם, תוך גילוי אורך רוח והבנה, מאפשרת לעורף המשפחתי לעמוד איתן ולסייע למשרתי המילואים להקדיש את כל כולם למשימה הלאומית.

מחויבותכם והערכים שאתם מייצגים מהווים נדבך מרכזי בעוצמתנו וביכולתה של החטיבה להמשיך ולפעול למען ביטחון המדינה.

אנו מודים לכם על היותכם חלק בלתי נפרד מהמאמץ הלאומי.

בהערכה רבה,אל"ם יוסי אליאס
מפקד חטיבת הנגב
"""
    EMAIL_SENDER_ADDRESS = "hative-mail-address"
    EMAIL_SENDER_PASSWORD = "email-password-16-chars"

    FONT_REGULAR = 'Rubik-Regular'
    FONT_SIZE_REGULAR = 16
    FONT_BOLD = 'Rubik-Bold'
    FONT_SIZE_BOLD = 26
    FONT_REGULAR_PATH = r'fonts/Rubik/static/Rubik-Regular.ttf'
    FONT_BOLD_PATH = r'fonts/Rubik/static/Rubik-Bold.ttf'

