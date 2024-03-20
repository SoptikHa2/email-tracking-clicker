from pydantic import BaseModel


class TrackingEntry(BaseModel):
    email_original_sender_regex: str
    links_to_click_regex: list[str]


class Config(BaseModel):
    email_address: str
    email_password: str
    imap_server: str

    whitelist: list[TrackingEntry]
