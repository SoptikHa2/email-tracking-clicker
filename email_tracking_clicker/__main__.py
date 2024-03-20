import os
import time

from email_tracking_clicker.checked_emails import load_checked_emails, save_checked_emails, update_stats_links_clicked
from email_tracking_clicker.config import Config
from email_extractor import EmailExtractor
from email_tracking_clicker.email_checker import check_emails


def main() -> None:
    with open(os.getenv("EMAIL_TRACKING_CLIENT_CONFIG", os.path.dirname(__file__) + '/../config/config.json')) as f:
        config = Config.model_validate_json(f.read())

    checked_entries = load_checked_emails()

    extractor = EmailExtractor(config.email_address, config.email_password, config.imap_server,
                               last_processed_id=checked_entries.email_to_last_id_done.get(config.email_address, None))
    extractor.connect()

    while True:
        links_clicked = check_emails(config, extractor)

        update_stats_links_clicked(links_clicked)

        checked_entries.email_to_last_id_done[config.email_address] = extractor.get_last_processed_id()
        save_checked_emails(checked_entries)

        print(f"Done, waiting {config.check_interval_s} seconds...")
        time.sleep(config.check_interval_s)



if __name__ == '__main__':
    main()
