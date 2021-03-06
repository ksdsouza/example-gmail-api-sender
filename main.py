from gmail import gmailClient


def main():
    gmailClient.send_email(
        receiver='ksdsouza@uwaterloo.ca',
        subject='Test gmail api message',
        body='Hello World!'
    )


if __name__ == '__main__':
    main()
