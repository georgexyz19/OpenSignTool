import gzip


def main():
    """Revert binary sign_letters to svg file"""

    with gzip.open('sign_letters', 'rb') as f:
        str_etree = f.read()

    with open('sign_letters.svg', 'w') as f:
        f.write(str_etree.decode())


if __name__ == '__main__':
    main()
