import mock
import os
import shutil
import tempfile
import six
from six.moves import reload_module
import unittest

from secretcrypt import local


class TestLocal(unittest.TestCase):

    def setUp(self):
        reload_module(local)
        self.tmpdir = tempfile.mkdtemp()
        self.key_file = os.path.join(self.tmpdir, 'key')
        self.patcher = mock.patch('secretcrypt.local._key_dir')
        mock_key_dir = self.patcher.start()
        mock_key_dir.return_value = self.tmpdir

    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @mock.patch('os.makedirs')
    def test_key_created(self, os_makedirs):
        local.encrypt(b'abc')
        os_makedirs.assert_called_with(self.tmpdir)
        self.assertTrue(os.path.isfile(self.key_file))

    def test_key_loaded(self):
        with open(self.key_file, 'wb') as f:
            f.write(os.urandom(16))
        with open(self.key_file) as f:
            with mock.patch.object(six.moves.builtins, 'open') as mock_open:
                mock_open.return_value = f
                local.encrypt(b'abc')
                mock_open.assert_called_with(self.key_file)

    def test_encrypt_decrypt(self):
        plaintext = b'myplaintext'
        ciphertext, decrypt_params = local.encrypt(plaintext)
        self.assertEqual(plaintext, local.decrypt(ciphertext, **decrypt_params))
