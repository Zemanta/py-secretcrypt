"""
Encrypted secrets.

Usage:
  decrypt-secret <secret>
"""
from __future__ import print_function
from docopt import docopt

from secretcrypt import Secret


def decrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    secret = Secret(arguments['<secret>'])
    return secret.decrypt()

if __name__ == '__main__':
    print(decrypt_secret_cmd())
