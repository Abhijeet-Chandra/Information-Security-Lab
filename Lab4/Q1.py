import os
import secrets

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# =========================================================
# PUBLIC DIFFIE-HELLMAN PARAMETERS
# =========================================================

P = 467
G = 2


# =========================================================
# SUBSYSTEM
# =========================================================

class Subsystem:

    def __init__(self, name):

        self.name = name
        self.active = True

        # ---------------------------------------------
        # RSA keys
        # ---------------------------------------------

        self.rsa_private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        self.rsa_public = self.rsa_private.public_key()

        # ---------------------------------------------
        # Diffie-Hellman keys
        # ---------------------------------------------

        self.dh_private = secrets.randbelow(P - 2) + 1

        self.dh_public = pow(
            G,
            self.dh_private,
            P
        )


# =========================================================
# KEY MANAGEMENT
# =========================================================

class KeyManager:

    def __init__(self):

        self.subsystems = {}


    # -----------------------------------------------------
    # Register a new subsystem
    # -----------------------------------------------------

    def register(self, subsystem):

        self.subsystems[subsystem.name] = subsystem

        print(
            subsystem.name,
            "registered successfully."
        )


    # -----------------------------------------------------
    # Revoke a subsystem
    # -----------------------------------------------------

    def revoke(self, name):

        if name in self.subsystems:

            self.subsystems[name].active = False

            print(
                name,
                "has been revoked."
            )


    # -----------------------------------------------------
    # Check whether subsystem is active
    # -----------------------------------------------------

    def is_active(self, name):

        return (
            name in self.subsystems
            and self.subsystems[name].active
        )


    # -----------------------------------------------------
    # Display registered subsystems
    # -----------------------------------------------------

    def display(self):

        print("\nRegistered Subsystems:")

        for name, system in self.subsystems.items():

            status = "Active" if system.active else "Revoked"

            print(
                name,
                "->",
                status
            )


# =========================================================
# DIFFIE-HELLMAN SHARED SECRET
# =========================================================

def generate_shared_secret(
        sender,
        receiver):

    # Sender calculates:
    # K = receiver_public ^ sender_private mod P

    sender_secret = pow(
        receiver.dh_public,
        sender.dh_private,
        P
    )

    # Receiver calculates:
    # K = sender_public ^ receiver_private mod P

    receiver_secret = pow(
        sender.dh_public,
        receiver.dh_private,
        P
    )

    return sender_secret, receiver_secret


# =========================================================
# DERIVE AES KEY FROM DH SECRET
# =========================================================

def derive_aes_key(shared_secret):

    # Convert integer shared secret into bytes

    secret_bytes = shared_secret.to_bytes(
        (shared_secret.bit_length() + 7) // 8,
        byteorder="big"
    )

    # SHA-256 gives us a 256-bit AES key

    digest = hashes.Hash(
        hashes.SHA256()
    )

    digest.update(secret_bytes)

    return digest.finalize()


# =========================================================
# RSA DIGITAL SIGNATURE
# =========================================================

def sign_message(sender, message):

    signature = sender.rsa_private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(
                hashes.SHA256()
            ),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


# =========================================================
# VERIFY RSA DIGITAL SIGNATURE
# =========================================================

def verify_signature(
        sender,
        message,
        signature):

    try:

        sender.rsa_public.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(
                    hashes.SHA256()
                ),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except Exception:

        return False


# =========================================================
# ENCRYPT DOCUMENT
# =========================================================

def encrypt_document(message, aes_key):

    aes = AESGCM(aes_key)

    nonce = os.urandom(12)

    ciphertext = aes.encrypt(
        nonce,
        message.encode(),
        None
    )

    return nonce, ciphertext


# =========================================================
# DECRYPT DOCUMENT
# =========================================================

def decrypt_document(
        nonce,
        ciphertext,
        aes_key):

    aes = AESGCM(aes_key)

    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode()


# =========================================================
# SECURE DOCUMENT TRANSFER
# =========================================================

def secure_transfer(
        sender,
        receiver,
        document):

    print("\n" + "=" * 60)

    print(
        "SECURE TRANSFER:",
        sender.name,
        "->",
        receiver.name
    )

    print("=" * 60)


    # -----------------------------------------------------
    # Check whether both systems are active
    # -----------------------------------------------------

    if not sender.active:

        print("Transfer failed: sender is revoked.")
        return

    if not receiver.active:

        print("Transfer failed: receiver is revoked.")
        return


    # -----------------------------------------------------
    # DIFFIE-HELLMAN
    # -----------------------------------------------------

    sender_secret, receiver_secret = \
        generate_shared_secret(
            sender,
            receiver
        )

    print(
        "\nDH shared secret same:",
        sender_secret == receiver_secret
    )


    # -----------------------------------------------------
    # AES KEY
    # -----------------------------------------------------

    aes_key = derive_aes_key(
        sender_secret
    )

    receiver_aes_key = derive_aes_key(
        receiver_secret
    )

    print(
        "AES key same:",
        aes_key == receiver_aes_key
    )


    # -----------------------------------------------------
    # RSA DIGITAL SIGNATURE
    # -----------------------------------------------------

    signature = sign_message(
        sender,
        document.encode()
    )

    print(
        "RSA signature verified:",
        verify_signature(
            sender,
            document.encode(),
            signature
        )
    )


    # -----------------------------------------------------
    # ENCRYPT DOCUMENT
    # -----------------------------------------------------

    nonce, ciphertext = encrypt_document(
        document,
        aes_key
    )

    print(
        "\nEncrypted document:"
    )

    print(
        ciphertext.hex()
    )


    # -----------------------------------------------------
    # DECRYPT DOCUMENT
    # -----------------------------------------------------

    decrypted = decrypt_document(
        nonce,
        ciphertext,
        receiver_aes_key
    )

    print(
        "\nDecrypted document:"
    )

    print(
        decrypted
    )


    # -----------------------------------------------------
    # FINAL VERIFICATION
    # -----------------------------------------------------

    print(
        "\nDocument verification:",
        decrypted == document
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 60)
    print("SECURECORP SECURE COMMUNICATION SYSTEM")
    print("=" * 60)


    # -----------------------------------------------------
    # Create key manager
    # -----------------------------------------------------

    key_manager = KeyManager()


    # -----------------------------------------------------
    # Create SecureCorp subsystems
    # -----------------------------------------------------

    finance = Subsystem("Finance System")
    hr = Subsystem("HR System")
    supply_chain = Subsystem("Supply Chain System")


    # -----------------------------------------------------
    # Register systems
    # -----------------------------------------------------

    key_manager.register(finance)
    key_manager.register(hr)
    key_manager.register(supply_chain)


    # -----------------------------------------------------
    # Display systems
    # -----------------------------------------------------

    key_manager.display()


    # -----------------------------------------------------
    # Finance -> HR
    # -----------------------------------------------------

    secure_transfer(
        finance,
        hr,
        "Confidential Employee Contract"
    )


    # -----------------------------------------------------
    # Finance -> Supply Chain
    # -----------------------------------------------------

    secure_transfer(
        finance,
        supply_chain,
        "Procurement Order"
    )


    # -----------------------------------------------------
    # Demonstrate scalability
    # -----------------------------------------------------

    marketing = Subsystem("Marketing System")

    key_manager.register(marketing)

    key_manager.display()


    # -----------------------------------------------------
    # Demonstrate key revocation
    # -----------------------------------------------------

    key_manager.revoke(
        "HR System"
    )

    key_manager.display()


    # -----------------------------------------------------
    # Try communication with revoked system
    # -----------------------------------------------------

    secure_transfer(
        finance,
        hr,
        "Financial Report"
    )


if __name__ == "__main__":
    main()