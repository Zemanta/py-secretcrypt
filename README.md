# py-secretcrypt

**WARNING**: this software is in alpha state, use with caution.

Utility for keeping your secrets encrypted. Also has a [Go version](https://github.com/Zemanta/go-secretcrypt).

For example, you have the following configuration file

```
MY_SECRET=VerySecretValue!
```

but you can't include that file in VCS because then your secret value would be exposed.

With **secretcrypt**, you can encrypt your secret using your AWS KMS master key aliased *MyKey*:

```bash
$ encrypt-secret kms alias/MyKey
Enter plaintext: VerySecretValue! # enter
kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE... # shortened for brevity

# --- or --
$ echo "VerySecretValue!" | encrypt-secret kms alias/MyKey  
kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE... # shortened for brevity
# only use piping when scripting, otherwise your secrets will be stored
# in your shell's history!

```

use that secret in my config file
```python
from secretcrypt import Secret
MY_SECRET=Secret('kms:region=us-east-1:CiC/SXeuXDGRADRIjc0qcE...')  # shortened for brevity
```

and get the plaintext like

```python
print MY_SECRET.decrypt()
# VerySecretValue!
```

## KMS
The KMS option uses AWS Key Management Service. When encrypting and decrypting
KMS secrets, you need to provide which AWS region the is to be or was encrypted
on, but it defaults to `us-east-1`.

So if you use a custom region, you must provide it to secretcrypt:

```bash
encrypt-secret kms --region us-west-1 alias/MyKey
```

## Local encryption
This mode is meant for local and/or offline development usage.
It generates a local key in your %USER_DATA_DIR%
(see [appdirs](https://pypi.python.org/pypi/appdirs)), so that the key cannot
be accidentally committed to CVS.

It then uses that key to symmetrically encrypt and decrypt your secrets.
