import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def decrypt_file(in_filename: str, password: str, out_filename: str = None):
    """
    Decrypts a file encrypted using AES-256-GCM and PBKDF2-HMAC-SHA256.

    Assumes file format:
    [0:16]   = salt
    [16:28]  = nonce
    [28:44]  = tag
    [44:]    = ciphertext

    Parameters:
    - in_filename: Path to the encrypted file (must match above format)
    - password: The password used during encryption
    - out_filename: Output path for the decrypted file (optional)

    Raises:
    - ValueError if decryption fails (bad password or tampering)

    Output:
    - The original decrypted file content
    """
    with open(in_filename, 'rb') as f:
        file_data = f.read()

    # Parse the structured components from encrypted data
    salt = file_data[:16]
    nonce = file_data[16:28]
    tag = file_data[28:44]
    ciphertext = file_data[44:]

    # Derive the same 256-bit key from password and salt
    key = PBKDF2(password, salt, dkLen=32, count=200_000)

    # Create AES cipher with same nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        # Decrypt and validate tag
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        raise ValueError("Decryption failed: wrong password or corrupted file")

    # Write decrypted content to output file
    out_filename = out_filename or in_filename.replace('.enc', '.dec')
    with open(out_filename, 'wb') as f:
        f.write(plaintext)

    print(f"Decrypted file saved as: {out_filename}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python decrypt_secure.py <input_file> <password>")
        sys.exit(1)

    decrypt_file(sys.argv[1], sys.argv[2])
