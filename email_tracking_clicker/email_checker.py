import re
import logging
import urllib.request

from email_tracking_clicker.config import Config
from email_tracking_clicker.email_extractor import EmailExtractor


def check_emails(config: Config, extractor: EmailExtractor) -> int:
    """
    Returns the number of clicked links
    """
    links_clicked = 0
    emails = extractor.get_new_emails()

    for email in emails:
        for entry in config.whitelist:
            if any(re.fullmatch(entry.email_original_sender_regex, sender) for sender in email.get_correspondents()):
                logging.info(f"Email from {email.get_correspondents()} matches {entry.email_original_sender_regex}")
                links = email.get_links()
                for link in links:
                    for regex in entry.links_to_click_regex:
                        if re.fullmatch(regex, link):
                            print(f"Clicking link {link} from {email.get_correspondents()}")

                            request = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
                                                                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                                                                            'Accept-Encoding': 'gzip, deflate, br'})

                            try:
                                with urllib.request.urlopen(request) as f:
                                    _ = f.read()  # trigger read, not sure if just opening it fetches it
                            except:
                                pass

                            links_clicked += 1

    return links_clicked
