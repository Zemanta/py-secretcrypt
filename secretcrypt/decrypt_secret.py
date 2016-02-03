"""
Encrypted secrets.

Usage:
  decrypt-secret [--region=<region_name>] <secret>

Options:
  --region=<region_name>    AWS Region Name [default: us-east-1]
"""
from __future__ import print_function
from docopt import docopt

from secretcrypt import Secret


def decrypt_secret_cmd():
    arguments = docopt(__doc__, options_first=True)
    if arguments['--region']:
        import kms
        kms.set_region(arguments['--region'])
    secret = Secret(arguments['<secret>'])
    return secret.decrypt()

if __name__ == '__main__':
    print(decrypt_secret_cmd())
