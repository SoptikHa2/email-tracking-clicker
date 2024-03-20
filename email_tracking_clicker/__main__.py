import os

from email_tracking_clicker.config import Config


def main() -> None:
    with open(os.getenv("EMAIL_TRACKING_CLIENT_CONFIG", os.path.dirname(__file__) + '/../config/config.json')) as f:
        config = Config.model_validate_json(f.read())
    pass


if __name__ == '__main__':
    main()
