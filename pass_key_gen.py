import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

backend = default_backend()
salt = b'\xd5z\xe49\xca\xd0\xa8\xd6\xb0\x0e\x1c\xc9\x80\xb2t2'

# Generate a key
# passw is the user password
# writeToFile is boolean
def gen_key(passw, writeToFile):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    # Generate key
    key = base64.urlsafe_b64encode(kdf.derive(passw.encode()))
    # Write to file if writeToFile is True else return the key
    if writeToFile:
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        return key
