"""Signature generation using openssl as a fallback when the python cryptography package is not available."""
from __future__ import absolute_import, print_function

import base64
import subprocess
import tempfile


def sign(payload):
    with tempfile.NamedTemporaryFile() as private_key_fd:
        run_command(['openssl', 'ecparam', '-genkey', '-name', 'secp384r1', '-noout', '-outform', 'der', '-out', private_key_fd.name])
        public_key_der = run_command(['openssl', 'ec', '-pubout', '-inform', 'der', '-outform', 'der', '-in', private_key_fd.name])
        signature = run_command(['openssl', 'dgst', '-sha256', '-keyform', 'der', '-sign', private_key_fd.name], payload)

    public_key_base64 = base64.b64encode(public_key_der).decode()
    signature_base64 = base64.b64encode(signature).decode()

    return public_key_base64, signature_base64


def run_command(cmd, data=None):
    if data is None:
        stdin = None
        data_bytes = None
    else:
        stdin = subprocess.PIPE
        data_bytes = data.encode()

    process = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(data_bytes)

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, cmd, stdout, stderr)

    return stdout
