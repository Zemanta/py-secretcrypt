import importlib
import six
from six.moves import urllib
import sys

CRYPTER_MODULES = [
    'local',
    'kms',
    'plain',
    'mock_crypter',
]


class Secret(object):
    """Represents an encrypted secret that can be decrypted on demand."""

    def __init__(self, secret):
        if len(secret) == 0:
            # empty secret object
            self._cached = True
            self.__plaintext = ''
            return

        tokens = secret.split(':')
        if len(tokens) < 3:
            raise ValueError('Malformed secret "%s"' % secret)

        crypter_name = tokens[0]
        if crypter_name not in CRYPTER_MODULES:
            raise ValueError(('Invalid encryption module in secret "%s": %s, ' +
                             'not one of %s') % (secret, crypter_name, CRYPTER_MODULES))
        try:
            self._crypter = importlib.import_module('.' + crypter_name.lower(), package=__name__)
        except ImportError as e:
            raise ValueError(('Problem importing encryption module "%s", are ' +
                             'you missing dependencies? %s') % (crypter_name, e))

        try:
            self._decrypt_params = {}
            if tokens[1]:
                params = urllib.parse.parse_qs(tokens[1], strict_parsing=True)
                self._decrypt_params = {k: v[0] for k, v in params.items()}
        except ValueError as e:
            raise ValueError('Invalid decryption parameters in secret "%s": %s' % (secret, e))

        self._ciphertext = ':'.join(tokens[2:])
        self._cached = False
        self.__plaintext = ''

    def decrypt(self):
        try:
            if self._cached:
                return self.__plaintext
            plaintext = self._crypter.decrypt(self._ciphertext, **self._decrypt_params)
            self.__plaintext = plaintext
            self._cached = True
            return plaintext
        except Exception as e:
            exc_info = sys.exc_info()
            six.reraise(
                ValueError('Invalid ciphertext "%s", error: %s' % (self._ciphertext, e)),
                None,
                exc_info[2]
            )

    def __str__(self):
        """Redacted string representation."""
        return '<redacted>'

    def __repr__(self):
        """Redacted repr representation."""
        return '<redacted>'
