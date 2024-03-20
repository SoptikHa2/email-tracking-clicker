import os

from pydantic import BaseModel


class CheckedEmails(BaseModel):
    email_to_last_id_done: dict[str, bytes]


def load_checked_emails() -> CheckedEmails:
    try:
        with open(f"{os.path.dirname(__file__)}/../config/checked_emails.json") as f:
            return CheckedEmails.model_validate_json(f.read())
    except:
        return CheckedEmails(email_to_last_id_done={})


def save_checked_emails(checked_emails: CheckedEmails) -> None:
    with open(f"{os.path.dirname(__file__)}/../config/checked_emails.json", "w") as f:
        f.write(checked_emails.json())


def update_stats_links_clicked(links_clicked: int) -> None:
    try:
        with open(f"{os.path.dirname(__file__)}/../config/stats.txt") as f:
            links_clicked += int(f.read())
    except:
        pass

    with open(f"{os.path.dirname(__file__)}/../config/stats.txt", "w") as f:
        f.write(str(links_clicked))
