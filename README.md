# RSA Secure Document Processor

A Python-based secure document processing tool that demonstrates RSA encryption, decryption, digital signing, and signature verification.

The project uses RSA-2048 with OAEP padding and SHA-256 for encryption, together with RSA PKCS#1 v1.5 signatures and SHA-256 for document authenticity and integrity verification.

## Features

* Generate a 2048-bit RSA public/private key pair
* Encrypt plaintext using RSA-OAEP with SHA-256
* Decrypt RSA-encrypted ciphertext
* Sign documents using RSA and SHA-256
* Verify digital signatures using the corresponding public key
* Store ciphertext and signatures in Base64 format
* Handle invalid keys, corrupted ciphertext, invalid signatures, and missing files

## Requirements

* Python 3.10+
* PyCryptodome

Install the required dependency:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python src/main.py
```

The program provides the following menu:

```text
1. Generate keys
2. Encrypt message
3. Decrypt ciphertext
4. Sign message
5. Verify signature
0. Exit
```

### Generate Keys

Generates:

```text
public.pem
private.pem
```

The private key should be kept secret and should not be committed to the repository.

### Encrypt a Message

The program reads:

```text
confidential_message.txt
```

and encrypts it using the RSA public key.

The resulting ciphertext is stored in:

```text
secure_message.enc
```

### Decrypt Ciphertext

The encrypted message is decrypted using the RSA private key and written to:

```text
plaintext.txt
```

### Sign a Message

The original message is hashed using SHA-256 and signed using the RSA private key.

The resulting signature is stored in:

```text
digital_signature.sig
```

### Verify a Signature

The program hashes the decrypted plaintext using SHA-256 and verifies the signature using the RSA public key.

A valid signature confirms that the message has not been modified and that the signature was generated using the corresponding private key.

## Cryptographic Design

### Encryption

```text
Plaintext
   ↓
RSA-OAEP + SHA-256
   ↓
Ciphertext
   ↓
Base64 Encoding
```

### Decryption

```text
Base64 Ciphertext
   ↓
Base64 Decoding
   ↓
RSA-OAEP + SHA-256
   ↓
Plaintext
```

### Digital Signature

```text
Document
   ↓
SHA-256
   ↓
Message Hash
   ↓
Sign with RSA Private Key
   ↓
PKCS#1 v1.5 Signature
   ↓
Base64 Encoding
```

### Signature Verification

```text
Document
   ↓
SHA-256
   ↓
Message Hash
   ↓
RSA PKCS#1 v1.5 Verification ← Signature
   ↑
Public Key
   ↓
Valid / Invalid
```

The private key is used to create the signature, while the corresponding public key is used to verify it.

## RSA-OAEP Message Size

The program uses a 2048-bit RSA key with OAEP and SHA-256.

The maximum plaintext size for direct RSA encryption is:

```text
256 - (2 × 32) - 2 = 190 bytes
```

Therefore, the program limits encrypted input to 190 bytes.

For larger documents, a practical system would normally use hybrid encryption, where a symmetric algorithm such as AES encrypts the document and RSA protects the symmetric key.

## Project Structure

```text
rsa-secure-document-processor/
├── src/
│   └── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

Generated private keys, ciphertext, signatures, and other sensitive files are excluded through `.gitignore`.

## Technologies

* Python
* PyCryptodome
* RSA-2048
* OAEP
* SHA-256
* PKCS#1 v1.5 digital signatures
* Base64

## Limitations

* Direct RSA encryption is limited to 190 bytes due to the RSA-2048 OAEP configuration.
* The program is intended as an educational implementation of public-key cryptography rather than a production document encryption system.
* Private keys are stored locally without password-based encryption.

## License

This project is licensed under the MIT License.
