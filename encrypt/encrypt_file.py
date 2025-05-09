import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def encrypt_file(in_filename: str, password: str, out_filename: str = None):
    """
    Encrypts a file using AES-256 in GCM mode and PBKDF2-HMAC-SHA256 key derivation.

    Format of output file (all binary):
    [0:16]   = salt (random)
    [16:28]  = nonce (random, 96 bits)
    [28:44]  = authentication tag (128 bits)
    [44:]    = ciphertext

    Parameters:
    - in_filename: Path to the plaintext input file
    - password: User-provided password (used as a key basis)
    - out_filename: Path for the encrypted output file (optional)

    Output:
    - A binary file containing the salt, nonce, auth tag, and ciphertext
    """
    # Generate 16-byte random salt
    salt = os.urandom(16)

    # Generate 12-byte nonce (recommended size for GCM)
    nonce = os.urandom(12)

    # Derive a 256-bit key (32 bytes) from password using PBKDF2-HMAC-SHA256
    key = PBKDF2(password, salt, dkLen=32, count=200_000)

    # Create AES-GCM cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # Read input plaintext
    with open(in_filename, 'rb') as f:
        plaintext = f.read()

    # Encrypt and produce authentication tag
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Compose final output file path
    out_filename = out_filename or (in_filename + '.enc')

    # Write salt + nonce + tag + ciphertext
    with open(out_filename, 'wb') as f:
        f.write(salt + nonce + tag + ciphertext)

    print(f"Encrypted file saved as: {out_filename}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python encrypt_secure.py <input_file> <password>")
        sys.exit(1)

    encrypt_file(sys.argv[1], sys.argv[2])
