py-secretcrypt
==============

|Circle CI|

**WARNING**: this software is in alpha state, use with caution.

Utility for keeping your secrets encrypted. Also has a `Go
version <https://github.com/Zemanta/go-secretcrypt>`__.

For example, you have the following configuration file

::

    MY_SECRET=VerySecretValue!

but you can't include that file in VCS because then your secret value
would be exposed.

With **secretcrypt**, you can encrypt your secret using your AWS KMS
master key aliased *MyKey*:

.. code:: bash

    $ encrypt-secret kms alias/MyKey
    Enter plaintext: VerySecretValue! # enter
    kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE... # shortened for brevity

    # --- or --
    $ echo "VerySecretValue!" | encrypt-secret kms alias/MyKey  
    kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE... # shortened for brevity
    # only use piping when scripting, otherwise your secrets will be stored
    # in your shell's history!

use that secret in my config file

.. code:: python

    from secretcrypt import Secret
    MY_SECRET=Secret('kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE...')  # shortened for brevity

and get the plaintext like

.. code:: python

    print MY_SECRET.get()
    # VerySecretValue!

If you are using very sensitive secrets, you can ensure the plaintext
is not kept in memory and is only encrypted on demand by using a stricter
version:

.. code:: python

    from secretcrypt import StrictSecret
    MY_SECRET=StrictSecret('kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE...')  # shortened for brevity

and get the plaintext like

.. code:: python

    print MY_SECRET.decrypt()
    # VerySecretValue!

KMS
---

The KMS option uses AWS Key Management Service. When encrypting and
decrypting KMS secrets, you need to provide which AWS region the is to
be or was encrypted on, but it defaults to ``us-east-1``.

So if you use a custom region, you must provide it to secretcrypt:

.. code:: bash

    encrypt-secret kms --region us-west-1 alias/MyKey

Local encryption
----------------

This mode is meant for local and/or offline development usage. It
generates a local key in your %USER\_DATA\_DIR% (see
`appdirs <https://pypi.python.org/pypi/appdirs>`__), so that the key
cannot be accidentally committed to CVS.

It then uses that key to symmetrically encrypt and decrypt your secrets.

.. |Circle CI| image:: https://circleci.com/gh/Zemanta/py-secretcrypt.svg?style=svg
   :target: https://circleci.com/gh/Zemanta/py-secretcrypt
