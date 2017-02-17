#!/usr/bin/env python

import datetime

from junit_xml import TestSuite, TestCase

test_cases = [
    # passing tests (those without error_info, failure_info, skipped_info) are counted but show no output in Shippable UI
    TestCase(name='test-case-name', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),

    # error tests show error message and error output in Shippable UI (but not stdout/stderr)
    TestCase(name='test-case-name-error', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    # failure tests show failure message and failure output in Shippable UI (but not stdout/stderr)
    TestCase(name='test-case-name-failure', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    # skipped tests are counted but show no output in Shippable UI
    TestCase(name='test-case-name-skipped', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),

    # more test cases
    TestCase(name='test-case-name-error-no-output', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    TestCase(name='test-case-name-failure-no-output', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    TestCase(name='test-case-name-skipped-no-output', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
]

test_cases[1].add_error_info(message='error message', output='error output')
test_cases[2].add_failure_info(message='failure message', output='failure output')
test_cases[3].add_skipped_info(message='skipped message', output='skipped output')

test_cases[4].add_error_info(message='error message')
test_cases[5].add_failure_info(message='failure message')
test_cases[6].add_skipped_info(message='skipped message')

test_suites = [
    TestSuite(
        name='test-suite-name',  # visible in Shippable UI
        test_cases=test_cases,  # visible in Shippable UI (see notes above)
        hostname='hostname',  # not visible in Shippable UI
        id='id',  # not visible in Shippable UI
        package='package',  # not visible in Shippable UI
        timestamp=datetime.datetime.utcnow().replace(microsecond=0).isoformat(),  # not visible in Shippable UI
        # not visible in Shippable UI
        properties=dict(
            hello='world',
            yes='no',
        ),
    ),
]

report = TestSuite.to_xml_string(test_suites=test_suites, prettyprint=True, encoding='utf-8')

with open('shippable/testresults/junit.xml', 'wb') as xml:
    xml.write(report.encode(encoding='utf-8', errors='strict'))
