from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import base64

def read_file(filename, mode):
    try:
        with open(filename, mode) as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return None
    except OSError:
        print(f"Error: Unable to read file {filename}")
        return None

def write_file(filename, content, mode):
    try:
        with open(filename, mode) as file:
            file.write(content)
    except OSError:
        print(f"Error: Unable to write to file {filename}")
        return False
    return True

def generate_keys():
    e = 65537 # public exponent
    bit = 2048
    key = RSA.generate(bits = bit, e = e)

    # Convert the key to a specific format such as
    # e.g., -----BEGIN PUBLIC KEY----- 
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    if not write_file("public.pem", public_key, "wb"):
        return
    if not write_file("private.pem", private_key, "wb"):
        return

    print("A 2048-bit key pair has been generated.")

def encrypt_document(input_file, public_key_file, output_file):
    pub_key = read_file(public_key_file, 'rb')
    if pub_key is None: return

    try:
        # Convert pub_key to an RSA key object
        public_key = RSA.import_key(pub_key) 
    except (ValueError, TypeError, IndexError):
        print("Error: Invalid or corrupted public key.")
        return
    
    # Read the input_file as bytes
    text = read_file(input_file, 'rb')
    if text is None: return

    if len(text) > 190:
        print("Error: Input file is too large to encrypt (limit: 190 bytes).")
        return

    # create a PKCS1OAEP_Cipher object with SHA256 hashing algorithm 
    # and the public key
    text_to_encrypt = PKCS1_OAEP.new(public_key, hashAlgo=SHA256) 
    # Pad the text and then encrypt it
    ciphertext = text_to_encrypt.encrypt(text)
    # Encode ciphertext bytes into Base64 format
    b64_text = base64.b64encode(ciphertext) 

    if write_file(output_file, b64_text, 'wb'): # write to file as bytes
        print(f"The message has been encrypted and written to {output_file}.")

def decrypt_document(input_file, private_key_file, output_file):
    priv_key = read_file(private_key_file, 'rb')
    if priv_key is None: return

    try:
        # Convert priv_key to an RSA key object
        private_key = RSA.import_key(priv_key) 
    except (ValueError, TypeError, IndexError):
        print("Error: Invalid or corrupted private key.")
        return
    
    # read the Base64 ciphertext
    b64_text = read_file(input_file, 'rb') 
    if b64_text is None: return

    try:
        # Decode Base64 to get the original encrypted bytes
        encrypted_bytes = base64.b64decode(b64_text, validate=True) 
        # create a PKCS1OAEP_Cipher object with SHA256 hashing algorithm 
        # and the private key
        cipher_to_decrypt = PKCS1_OAEP.new(private_key, hashAlgo=SHA256) 
        # Decrypt the cipher and then remove the OAEP padding 
        decrypted_text = cipher_to_decrypt.decrypt(encrypted_bytes)
        
        # write to output_file as bytes
        if write_file(output_file, decrypted_text, 'wb'):
            print(f"The message has been decrypted and written to {output_file}.")
    except (ValueError, TypeError):
        print("Error: Decryption failed. The key may be invalid or the ciphertext is corrupted.")
    
def sign_document(input_file, private_key_file, signature_file):
    priv_key = read_file(private_key_file, 'rb')
    if priv_key is None: return

    try:
        # Convert priv_key to an RSA key object
        private_key = RSA.import_key(priv_key) 
    except (ValueError, TypeError, IndexError):
        print("Error: Invalid or corrupted private key.")
        return

    # Read the original text file, hash (SHA256) and sign the text 
    # with the private key. After that encode the signed bytes into 
    # Base64 format and write to digital_signature.sig
    text = read_file(input_file, 'rb')
    if text is None: return
    
    sha256_hash = SHA256.new(text)
    signature = pkcs1_15.new(private_key).sign(sha256_hash)
    b64_signature = base64.b64encode(signature)

    if write_file(signature_file, b64_signature, 'wb'):
        print(f"The message has been signed and written to {signature_file}.")

def verify_sign(input_file, signature_file, public_key_file):
    pub_key = read_file(public_key_file, 'rb')
    if pub_key is None: return

    try:
        # Convert pub_key to an RSA key object
        public_key = RSA.import_key(pub_key) 
    except (ValueError, TypeError, IndexError):
        print("Error: Invalid or corrupted public key.")
        return
    
    # After decrypted the ciphertext and get the plaintext.txt, 
    # hash (SHA256) the content in plaintext.txt. 
    # Now, read digital_signature.sig and decode Base64 to bytes. 
    text = read_file(input_file, 'rb')
    if text is None: return
    
    expected_hash = SHA256.new(text)

    sign = read_file(signature_file, 'rb')
    if sign is None: return

    try:
        signature = base64.b64decode(sign, validate=True)
    except (ValueError, TypeError):
        print("WARNING: The signature is invalid.")
        return

    # Verify() function will decrypt the signature with public_key 
    # and compare the hash value between expected_hash and signature
    # If they are identical, indicate the validity, vice versa.
    try:
        pkcs1_15.new(public_key).verify(expected_hash, signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
        print("WARNING: The signature is invalid.")

def RSA_menu():
    print("1. Generate keys")
    print("2. Encrypt message")
    print("3. Decrypt ciphertext")
    print("4. Sign message")
    print("5. Verify signature")
    print("0. Exit")
    menu_choice = int(input(">> "))

    return menu_choice
    
def main():
    menu_choice = -1
    priv_key_file = "private.pem"
    pub_key_file = "public.pem"
    message_file = "confidential_message.txt"
    ciphertext_file = "secure_message.enc"
    plaintext_file = "plaintext.txt"
    signature_file = "digital_signature.sig"

    while menu_choice != 0:
        try:
            menu_choice = RSA_menu()
        except ValueError:
            print("Error: Invalid input. Please enter an integer.\n")
            continue

        match menu_choice:
            case 1:
                generate_keys()
            case 2:
                encrypt_document(message_file, pub_key_file, ciphertext_file)
            case 3:
                decrypt_document(ciphertext_file, priv_key_file, plaintext_file)
            case 4:
                sign_document(message_file, priv_key_file, signature_file)
            case 5:
                verify_sign(plaintext_file, signature_file, pub_key_file)
            case 0:
                print("Program ends. Exiting...")
            case _:
                print("Error: Invalid command.")
        print() # Just for formatting

if __name__ == "__main__":
    main()
