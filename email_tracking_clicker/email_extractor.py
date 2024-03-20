import base64
import binascii
from contextlib import suppress
from imaplib import IMAP4
import logging

from email_tracking_clicker.mail import Email


class EmailExtractor:
    def __init__(self, email: str, password: str, imap: str, last_processed_id: bytes | None = None):
        self._email = email
        self._password = password
        self._imap = IMAP4(imap)
        self._last_processed_id = last_processed_id

    def connect(self):
        self._imap.login(self._email, self._password)
        self._imap.select()

    def get_new_emails(self) -> list[Email]:
        print('Checking emails...')
        _, data = self._imap.search(None, 'ALL')
        email_ids = data[0].split()  # those are numbers in bytes
        emails = []
        for email_id in email_ids:
            # Skip already processed email IDs
            if int(email_id.decode('utf-8')) <= int((self._last_processed_id or b'-1').decode('utf-8')):
                logging.debug(f"Skipping email ID {email_id}")
                continue
            else:
                logging.debug(f"Processing email ID {email_id}")
                self._last_processed_id = email_id

            _, data = self._imap.fetch(email_id, '(RFC822)')
            email_body_raw = data[0][1]

            # Decode the email body
            # first few rows are headers, than there is base64 encoded body, the last few lines are something else as well.
            # This is hacky, but it works for now.
            # We support only base64
            body_lines = []
            for line in email_body_raw.split(b'\r\n'):
                with suppress(binascii.Error, UnicodeDecodeError):
                    body_lines.append(base64.b64decode(line).decode('utf-8'))

            emails.append(Email(''.join(body_lines)))

        return emails

    def get_last_processed_id(self) -> bytes | None:
        return self._last_processed_id
