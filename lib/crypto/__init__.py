import lib.crypto.cryptography
import lib.crypto.openssl


def sign(payload):
    try:
        return lib.crypto.cryptography.sign(payload)
    except ImportError:
        return lib.crypto.openssl.sign(payload)
