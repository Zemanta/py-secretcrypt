import importlib
import six
from six.moves import urllib
import sys

CRYPTER_MODULES = [
    'local',
    'kms',
    'plain',
    'password',
    'mock_crypter',
]


class StrictSecret(object):
    """Represents an encrypted secret that can be decrypted on demand.

    Decrypting this secret may incur a side-effect such as a call to a remote
    service for decryption.
    """

    def __init__(self, secret):
        if len(secret) == 0:
            # empty secret object
            self._crypter = None
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

        ciphertext = ':'.join(tokens[2:])
        if isinstance(ciphertext, six.string_types):
            ciphertext = ciphertext.encode('utf-8')  # convert to bytes
        self._ciphertext = ciphertext

    def decrypt(self):
        """Decrypt decrypts the secret and returns the plaintext.

        Calling decrypt() may incur side effects such as a call to a remote service for decryption.
        """
        if not self._crypter:
            return b''
        try:
            plaintext = self._crypter.decrypt(self._ciphertext, **self._decrypt_params)
            return plaintext
        except Exception as e:
            exc_info = sys.exc_info()
            six.reraise(
                ValueError,
                ValueError('Invalid ciphertext "%s", error: %s' % (self._ciphertext, e)),
                exc_info[2]
            )

    def __str__(self):
        """Redacted string representation."""
        return '<redacted>'

    def __repr__(self):
        """Redacted repr representation."""
        return '<redacted>'


class Secret(object):
    """Represents a secret that is eagerly decrypted on object creation.

    After that, using this secret does not incur any side effects.
    """

    def __init__(self, secret):
        self.__plaintext_bytes = None
        self.__plaintext_bytes = StrictSecret(secret).decrypt()

    def get(self):
        """Return the secret in plain text.

        Calling get() does not incur any side effects.
        """
        return self.__plaintext_bytes

    def __str__(self):
        """Redacted string representation."""
        return '<redacted>'

    def __repr__(self):
        """Redacted repr representation."""
        return '<redacted>'
