from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='secretcrypt',
    packages=['secretcrypt'],
    version='0.2',
    description='Encrypt project secrets',
    author='Nejc Saje, Zemanta',
    author_email='nejc@saje.info',
    url='https://github.com/Zemanta/secretcrypt',
    download_url='https://github.com/Zemanta/secretcrypt/tarball/0.1',
    keywords=['secret', 'encrypt', 'decrypt', 'settings'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'encrypt-secret = secretcrypt.encrypt_secret:encrypt_secret_cmd',
            'decrypt-secret = secretcrypt.decrypt_secret:decrypt_secret_cmd',
        ],
    },
    install_requires=[
        'docopt==0.6.2',
        'six==1.10.0',
        'boto3==1.2.3',
        'pyaes==1.3.0',
    ],
    tests_require=['tox', 'virtualenv'],
    cmdclass={'test': Tox},
)
