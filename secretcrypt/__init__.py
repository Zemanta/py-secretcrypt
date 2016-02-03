import importlib
import six
import sys


class Secret(object):
    """Represents an encrypted secret that can be decrypted on demand."""

    def __init__(self, secret):
        self.secret = secret

    def decrypt(self):
        class_name, ciphertext = self.secret.split(':')
        try:
            crypter = importlib.import_module(class_name.lower(), package=__name__)
            return crypter.decrypt(ciphertext)
        except Exception as e:
            exc_info = sys.exc_info()
            six.reraise(ValueError('Invalid secret "%s", error: %s' % (self.secret, e)), None, exc_info[2])

    def __str__(self):
        """Redacted string representation."""
        return '<redacted>'

    def __repr__(self):
        """Redacted repr representation."""
        return '<redacted>'
