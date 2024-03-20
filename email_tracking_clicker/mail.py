import re

class Email:
    _LINK_REGEX = re.compile(
        r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\]>\)\s]*)?'
        , re.IGNORECASE)

    def __init__(self, raw_body: str):
        self._raw_body = raw_body

    def get_links(self) -> list[str]:
        text = self.get_text()

        return [
            link.removesuffix('>').removesuffix(']')
            for link in
            Email._LINK_REGEX.findall(text)
        ]


    def get_sender(self) -> str:
        lines = self._raw_body.split("\r\n")
        from_line = next(line for line in lines if line.startswith("From:"))
        email = re.search(r"<(.*?)>", from_line).group(1)
        return email

    def get_text(self) -> str:
        # First line: empty
        # Second line: separator
        # Next N lines: headers
        # N+1th line: empty
        # all other lines: body
        headers_and_text = self._raw_body.split("\r\n")[2:]
        while headers_and_text[0] != '':
            headers_and_text = headers_and_text[1:]

        return "\r\n".join(headers_and_text[1:])
