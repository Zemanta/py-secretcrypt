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

with open('README.rst') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()
history = history.replace(".. :changelog:", "")

setup(
    name='secretcrypt',
    packages=['secretcrypt'],
    version='1.0.4',
    description='Encrypt project secrets',
    long_description=readme + '\n\n' + history,
    author='Nejc Saje, Zemanta',
    author_email='nejc@saje.info',
    url='https://github.com/Zemanta/secretcrypt',
    download_url='https://github.com/Zemanta/secretcrypt/tarball/0.1',
    keywords=['secret', 'encrypt', 'decrypt', 'settings'],
    entry_points={
        'console_scripts': [
            'encrypt-secret = secretcrypt.encrypt_secret:encrypt_secret_cmd',
            'decrypt-secret = secretcrypt.decrypt_secret:decrypt_secret_cmd',
        ],
    },
    install_requires=[
        'docopt>=0.6.2',
        'six>=1.10.0',
        'boto3>=1.4',
        'pyaes>=1.6.0',
        'pyscrypt>=1.6.2',
    ],
    tests_require=['tox', 'virtualenv'],
    cmdclass={'test': Tox},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Security :: Cryptography',
    ],
)
