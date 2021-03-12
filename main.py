import os

from gmail import gmailClient


def main():
    gmailClient.send_email(
        receiver=os.environ.get("EMAIL", "default_email"),
        subject='Test gmail api message',
        body='Hello World!'
    )


if __name__ == '__main__':
    main()
