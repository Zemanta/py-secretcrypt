# secretcrypt

Utility for keeping your secrets encrypted.

For example, you have the following configuration file

```
MY_SECRET=VerySecretValue!
```

but you can't include that file in CVS because then your secret value would be exposed.

With **secretcrypt**, you can encrypt your secret using your AWS KMS master key aliased *MyKey*:

```
$ encrypt-secret kms alias/MyKey VerySecretValue!
KMS:CiC/SXeuXDGRADRIjc0qcE... # shortened for brevity

```

use that secret in my config file
```
from secretcrypt import secret
MY_SECRET=Secret('KMS:CiC/SXeuXDGRADRIjc0qcE...')  # shortened for brevity
```

and get the plaintext like

```
print MY_SECRET.decrypt()
# VerySecretValue!
```

## KMS
The KMS option uses AWS Key Management Service. When encrypting and decrypting
KMS secrets, you need to provide which AWS region the is to be or was encrypted
on, but it defaults to `us-east-1`.

Encrypting: `encrypt-secret kms --region us-west-1 alias/MyKey <plaintext>`

Decrypting:

```
from secretcrypt import Secret
from secretcrypt.kms import KMS

KMS.set_region('us-west-1')

Secret('KMS:CiC/SXeuXDGRADRIjc0qcE...').decrypt()

```

## Local encryption
This mode is meant for local and/or offline development usage.
It generates a local key in your %USER_DATA_DIR%
(see [appdirs](https://pypi.python.org/pypi/appdirs)), so that the key cannot
be accidentally committed to CVS.

It then uses that key to symmetrically encrypt and decrypt your secrets.
