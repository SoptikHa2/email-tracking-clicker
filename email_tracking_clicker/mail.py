import re

class Email:
    _LINK_REGEX = re.compile(
        r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\]>\)\s]*)?'
        , re.IGNORECASE)

    def __init__(self, body_lines: list[str]):
        self._body_lines = [body_line.replace("\n","").replace("\r", "").strip() for body_line in body_lines]
        self._raw_body = "".join(self._body_lines)

    def get_links(self) -> list[str]:
        return [
            link.split('>')[0].split('<')[0].split(']')[0].split("\"")[0].split("&nbsp")[0].removesuffix(".").removesuffix(";")
            for link in
            Email._LINK_REGEX.findall(self._raw_body)
        ]


    def get_correspondents(self) -> list[str]:
        return re.findall(r"<([^>]*@[^>]*)>", self._raw_body)
