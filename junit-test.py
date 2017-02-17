#!/usr/bin/env python

import datetime

from junit_xml import TestSuite, TestCase

test_cases = [
    TestCase(name='test-case-name-error', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    TestCase(name='test-case-name-failure', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    TestCase(name='test-case-name-skipped', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
]

test_cases[0].add_error_info(message='error message', output='error output')
test_cases[1].add_failure_info(message='failure message', output='failure output')
test_cases[2].add_skipped_info(message='skipped message', output='skipped output')

test_suites = [
    TestSuite(
        name='test-suite-name',
        test_cases=test_cases,
        hostname='hostname',
        id='id',
        package='package',
        timestamp=datetime.datetime.utcnow().replace(microsecond=0).isoformat(),
        properties=dict(
            hello='world',
            yes='no',
        ),
    ),
]

report = TestSuite.to_xml_string(test_suites=test_suites, prettyprint=True, encoding='utf-8')

with open('shippable/testresults/junit.xml', 'wb') as xml:
    xml.write(report.encode(encoding='utf-8', errors='strict'))
