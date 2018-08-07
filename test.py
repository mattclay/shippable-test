#!/usr/bin/env python3.6

import os
import time
import json

from lib.http import HttpClient, HttpError
from lib.util import display
from lib.crypto import sign


def main():
    endpoint = 'https://u79skqnq56.execute-api.us-east-1.amazonaws.com/dev/auth'
    job_id = os.environ['JOB_ID']

    public_key, signature = sign(job_id)

    display.info(f'-----BEGIN PUBLIC KEY----- {public_key} -----END PUBLIC KEY-----')

    payload = dict(
        job_id=job_id,
        signature=signature,
    )

    data = json.dumps(payload)

    http = HttpClient()

    for sleep_seconds in range(1, 5):
        response = http.post(endpoint, data)

        try:
            if response.status_code == 200:
                display.info(response.json())
                exit(0)

            display.info(response.json())
        except HttpError as ex:
            display.info(ex)

        time.sleep(sleep_seconds)

    exit(1)


if __name__ == '__main__':
    main()
