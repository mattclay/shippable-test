from __future__ import absolute_import, print_function

import base64


def sign(payload):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec

    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key_der = private_key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    signature = private_key.sign(payload.encode(), ec.ECDSA(hashes.SHA256()))

    public_key_base64 = base64.b64encode(public_key_der).decode()
    signature_base64 = base64.b64encode(signature).decode()

    return public_key_base64, signature_base64
