import argparse
import os
import secrets
import struct
import getpass
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Constants
CHUNK_SIZE = 64 * 1024  # 64 KB
MAGIC_HEADER = b"JON1"

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 32-byte key from a password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return kdf.derive(password.encode())

def process_file(file_path, password, mode):
    """Encrypts or decrypts a single file using ChaCha20-Poly1305."""
    file_name = os.path.basename(file_path)
    temp_file = file_path + ".tmp"

    try:
        # ===================== ENCRYPTION =====================
        if mode == "enc":
            if file_path.endswith(".enc") or file_path.endswith(".py"):
                return

            salt = secrets.token_bytes(16)
            key = derive_key(password, salt)
            chacha = ChaCha20Poly1305(key)

            with open(file_path, "rb") as f_in, open(temp_file, "wb") as f_out:
                f_out.write(MAGIC_HEADER)
                f_out.write(salt)

                while True:
                    chunk = f_in.read(CHUNK_SIZE)
                    if not chunk:
                        break

                    nonce = secrets.token_bytes(12)
                    ciphertext = chacha.encrypt(nonce, chunk, None)

                    # Store chunk length, nonce, and ciphertext
                    f_out.write(struct.pack(">I", len(ciphertext)))
                    f_out.write(nonce)
                    f_out.write(ciphertext)

            final_path = file_path + ".enc"
            os.replace(temp_file, final_path)
            if os.path.exists(file_path) and final_path != file_path:
                os.remove(file_path)
            print(f"🔒 Encrypted: {file_name}")

        # ===================== DECRYPTION =====================
        elif mode == "dec":
            if not file_path.endswith(".enc"):
                return

            with open(file_path, "rb") as f_in:
                # Check Magic Header
                if f_in.read(4) != MAGIC_HEADER:
                    raise ValueError("Invalid file format (JON1 header missing)")

                salt = f_in.read(16)
                key = derive_key(password, salt)
                chacha = ChaCha20Poly1305(key)

                original_path = file_path.rsplit(".enc", 1)[0]

                with open(temp_file, "wb") as f_out:
                    while True:
                        length_bytes = f_in.read(4)
                        if not length_bytes:
                            break

                        block_len = struct.unpack(">I", length_bytes)[0]
                        nonce = f_in.read(12)
                        ciphertext = f_in.read(block_len)

                        decrypted_chunk = chacha.decrypt(nonce, ciphertext, None)
                        f_out.write(decrypted_chunk)

            os.replace(temp_file, original_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            print(f"🔓 Decrypted: {file_name}")

    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"⚠️ Error ({file_name}): Authentication failed or corrupted file.")

def main():
    parser = argparse.ArgumentParser(description="JON1 Secure File Encryptor (ChaCha20-Poly1305)")
    parser.add_argument("-m", "--mode", choices=["enc", "dec"], required=True, help="Mode: enc (encrypt) or dec (decrypt)")
    parser.add_argument("-p", "--path", required=True, help="Path to file or directory")
    parser.add_argument("-pw", "--password", help="Password (Leave empty for secure prompt)")
    
    args = parser.parse_args()

    # Get password securely if not provided
    pwd = args.password
    if not pwd:
        pwd = getpass.getpass("Enter Encryption Key: ")

    if os.path.isfile(args.path):
        process_file(args.path, pwd, args.mode)
    elif os.path.isdir(args.path):
        print(f"📁 Processing directory: {args.path}")
        for root, _, files in os.walk(args.path):
            for file in files:
                if not file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    process_file(full_path, pwd, args.mode)
    else:
        print("❌ Error: Invalid path.")

if __name__ == "__main__":
    main()
