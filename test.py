#!/usr/bin/env python3.6

# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, serialization
# from cryptography.hazmat.primitives.asymmetric import ec

import base64
import datetime
import os
import requests
import time
import subprocess


# def sign_cryptography(data_string):
#     private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
#     public_key = private_key.public_key()
#
#     serialized_public = public_key.public_bytes(
#         encoding=serialization.Encoding.DER,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo)
#
#     data = data_string.encode('utf-8')
#
#     signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
#
#     b64_key = base64.b64encode(serialized_public).decode('utf-8')
#
#     serialized_public_string = f'-----BEGIN PUBLIC KEY----- {b64_key} -----END PUBLIC KEY-----'
#
#     signature_string = base64.b64encode(signature).decode('utf-8')
#
#     return serialized_public_string, signature_string


def sign_openssl(data_string):
    with open('data.txt', 'w') as fd:
        fd.write(data_string)

    subprocess.check_output(['openssl', 'ecparam', '-name', 'secp384r1', '-genkey', '-noout', '-out', 'private.der', '-outform', 'der'])
    subprocess.check_output(['openssl', 'ec', '-in', 'private.der', '-inform', 'der', '-pubout', '-out', 'public.der', '-outform', 'der'])
    subprocess.check_output(['openssl', 'dgst', '-sha256', '-sign', 'private.der', '-keyform', 'der', '-out', 'signature.out', 'data.txt'])

    with open('private.der', 'rb') as fd:
        serialized_public = fd.read()

    with open('signature.out', 'rb') as fd:
        signature = fd.read()

    b64_key = base64.b64encode(serialized_public).decode('utf-8')

    serialized_public_string = f'-----BEGIN PUBLIC KEY----- {b64_key} -----END PUBLIC KEY-----'

    signature_string = base64.b64encode(signature).decode('utf-8')

    return serialized_public_string, signature_string


def output(message):
    print(message, flush=True)


def main():
    endpoint = 'https://u79skqnq56.execute-api.us-east-1.amazonaws.com/dev/auth'
    job_id = os.environ['JOB_ID']

    output(f'job_id: {job_id}')

    # public_key, signature = sign_cryptography(job_id)
    public_key, signature = sign_openssl(job_id)

    output(public_key)

    payload = dict(
        job_id=job_id,
        signature=signature,
    )

    for attempt in range(1, 5):
        output(f'attempt #{attempt}')

        try:
            response = requests.post(endpoint, json=payload)

            if response.status_code == 200:
                output(response.content)
                output('success')
                exit(0)
            else:
                try:
                    message = response.json()['message']
                    output(f'ERROR: {message}')
                except ValueError:
                    output(response.content)
        except requests.RequestException as ex:
            output(ex)
            pass

        time.sleep(1)

    output('failed')
    exit(1)


if __name__ == '__main__':
    main()
