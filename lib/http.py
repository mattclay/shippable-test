"""
Primitive replacement for requests to avoid extra dependency.
Avoids use of urllib2 due to lack of SNI support.
"""

from __future__ import absolute_import, print_function

import json
import subprocess
import time

from lib.util import display

try:
    from urllib import urlencode
except ImportError:
    # noinspection PyCompatibility, PyUnresolvedReferences
    from urllib.parse import urlencode  # pylint: disable=locally-disabled, import-error, no-name-in-module

try:
    # noinspection PyCompatibility
    from urlparse import urlparse, urlunparse, parse_qs
except ImportError:
    # noinspection PyCompatibility, PyUnresolvedReferences
    from urllib.parse import urlparse, urlunparse, parse_qs  # pylint: disable=locally-disabled, ungrouped-imports


class HttpClient(object):
    """Make HTTP requests via curl."""
    def __init__(self, insecure=False):
        """
        :type insecure: bool
        """
        self.insecure = insecure

        self.username = None
        self.password = None

    def get(self, url):
        """
        :type url: str
        :rtype: HttpResponse
        """
        return self.request('GET', url)

    def delete(self, url):
        """
        :type url: str
        :rtype: HttpResponse
        """
        return self.request('DELETE', url)

    def put(self, url, data=None, headers=None):
        """
        :type url: str
        :type data: str | None
        :type headers: dict[str, str] | None
        :rtype: HttpResponse
        """
        return self.request('PUT', url, data, headers)

    def post(self, url, data=None, headers=None):
        """
        :type url: str
        :type data: str | None
        :type headers: dict[str, str] | None
        :rtype: HttpResponse
        """
        return self.request('POST', url, data, headers)

    def request(self, method, url, data=None, headers=None):
        """
        :type method: str
        :type url: str
        :type data: str | None
        :type headers: dict[str, str] | None
        :rtype: HttpResponse
        """
        cmd = ['curl', '-s', '-S', '-i', '-X', method]

        if self.insecure:
            cmd += ['--insecure']

        if headers is None:
            headers = {}

        headers['Expect'] = ''  # don't send expect continue header

        if self.username:
            if self.password:
                cmd += ['-u', '%s:%s' % (self.username, self.password)]
            else:
                cmd += ['-u', self.username]

        for header in headers.keys():
            cmd += ['-H', '%s: %s' % (header, headers[header])]

        if data is not None:
            cmd += ['-d', data]

        cmd += [url]

        attempts = 0
        max_attempts = 3
        sleep_seconds = 3

        # curl error codes which are safe to retry (request never sent to server)
        retry_on_status = (
            6,  # CURLE_COULDNT_RESOLVE_HOST
        )

        while True:
            attempts += 1

            try:
                stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT,)
                break
            except subprocess.CalledProcessError as ex:
                if ex.returncode in retry_on_status and attempts < max_attempts:
                    display.info(u'%s' % ex)
                    time.sleep(sleep_seconds)
                    continue

                raise

        header, body = stdout.decode('utf-8').split('\r\n\r\n', 1)

        response_headers = header.split('\r\n')
        first_line = response_headers[0]
        http_response = first_line.split(' ')
        status_code = int(http_response[1])

        return HttpResponse(method, url, status_code, body)


class HttpResponse(object):
    """HTTP response from curl."""
    def __init__(self, method, url, status_code, response):
        """
        :type method: str
        :type url: str
        :type status_code: int
        :type response: str
        """
        self.method = method
        self.url = url
        self.status_code = status_code
        self.response = response

    def json(self):
        """
        :rtype: any
        """
        try:
            return json.loads(self.response)
        except ValueError:
            raise HttpError(self.status_code, 'Cannot parse response to %s %s as JSON:\n%s' % (self.method, self.url, self.response))


class HttpError(Exception):
    """HTTP response as an error."""
    def __init__(self, status, message):
        """
        :type status: int
        :type message: str
        """
        super(HttpError, self).__init__('%s: %s' % (status, message))
        self.status = status
