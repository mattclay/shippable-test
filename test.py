#!/usr/bin/env python

import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib2
import uuid


def prepare_core_ci_auth():
    """Return authentication details for Ansible Core CI."""
    request = dict(
        run_id=os.environ['SHIPPABLE_BUILD_ID'],
        job_number=int(os.environ['SHIPPABLE_JOB_NUMBER']),
    )

    # sign_request(request)

    auth = dict(
        shippable=request,
    )

    return auth


def sign_request(request):
    """Sign the given auth request and make the public key available."""
    payload_bytes = json.dumps(request, sort_keys=True).encode()
    public_key_pem_bytes, signature_base64_string = sign_bytes(payload_bytes)

    publish_public_key(public_key_pem_bytes)

    request.update(signature=signature_base64_string)


def sign_bytes(payload_bytes):
    """
    Generate a private key and then sign the given bytes.
    Returns the PEM public key bytes and the base64 encoded signature string.
    """
    with open(os.devnull, 'wb') as devnull:
        private_key_pem_bytes = subprocess.check_output(['openssl', 'ecparam', '-genkey', '-name', 'secp384r1', '-noout'], stderr=devnull)

        p = subprocess.Popen(['openssl', 'ec', '-pubout'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=devnull)
        public_key_pem_bytes = p.communicate(private_key_pem_bytes)[0]

        with tempfile.NamedTemporaryFile() as private_key_file:
            private_key_file.write(private_key_pem_bytes)
            private_key_file.flush()

            with tempfile.NamedTemporaryFile() as payload_file:
                payload_file.write(payload_bytes)
                payload_file.flush()

                signature_bytes = subprocess.check_output(['openssl', 'dgst', '-sha256', '-sign', private_key_file.name, payload_file.name], stderr=devnull)

    signature_base64_string = base64.b64encode(signature_bytes).decode()

    return public_key_pem_bytes, signature_base64_string


def publish_public_key(public_key_pem_bytes):
    """Publish the given public key."""
    public_key_pem_string = public_key_pem_bytes.decode()
    # display the public key as a single line to avoid mangling such as when prefixing each line with a timestamp
    sys.stdout.write(public_key_pem_string.replace('\n', ' ') + '\n')
    sys.stdout.flush()
    # allow time for logs to become available to reduce repeated API calls
    time.sleep(3)


class MethodRequest(urllib2.Request):
    """HTTP request supporting arbitrary HTTP methods."""
    def __init__(self, method, *args, **kwargs):
        urllib2.Request.__init__(self, *args, **kwargs)
        self._method = method

    def get_method(self):
        """Return the HTTP method to use for the HTTP request."""
        return self._method


def main():
    auth = prepare_core_ci_auth()
    url = 'https://14blg63h2i.execute-api.us-east-1.amazonaws.com/dev/jobs/%s' % uuid.uuid4()

    headers = {
        'Content-Type': 'application/json',
    }

    print(url)

    data = dict(
        config=dict(
            platform='aws',
            version='sts',
        )
    )

    data.update(dict(auth=auth))

    request = MethodRequest('PUT', url, json.dumps(data), headers)

    try:
        response = urllib2.urlopen(request)
        print('OK')
    except urllib2.HTTPError as ex:
        print(ex.getcode())
        print(ex.read())


if __name__ == '__main__':
    main()
