"""
Encrypted secrets.

Usage:
  decrypt-secret <secret>
"""
from __future__ import print_function
from docopt import docopt

from secretcrypt import StrictSecret


def decrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    secret = StrictSecret(arguments['<secret>'])
    print(secret.decrypt().decode('utf-8'))

if __name__ == '__main__':
    decrypt_secret_cmd()
