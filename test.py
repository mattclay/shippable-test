#!/usr/bin/env python3.6

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

import os
import base64
import requests
import time


def sign(data_string):
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key = private_key.public_key()

    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    data = data_string.encode('utf-8')

    signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))

    serialized_public_string = serialized_public.decode('utf-8')

    signature_string = base64.b64encode(signature).decode('utf-8')

    return serialized_public_string, signature_string


def output(message):
    print(message, flush=True)


def main():
    endpoint = 'https://u79skqnq56.execute-api.us-east-1.amazonaws.com/dev/auth'
    job_id = os.environ['JOB_ID']

    output(f'job_id: {job_id}')

    public_key, signature = sign(job_id)

    output(public_key.strip())

    payload = dict(
        job_id=job_id,
        signature=signature,
    )

    for attempt in range(1, 10):
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

        time.sleep(3)

    output('failed')
    exit(1)


if __name__ == '__main__':
    main()
