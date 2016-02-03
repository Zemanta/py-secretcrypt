from setuptools import setup

setup(
    name='secretcrypt',
    packages=['secretcrypt'],
    version='0.1',
    description='Encrypt project secrets',
    author='Nejc Saje',
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
)
