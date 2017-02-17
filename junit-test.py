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

    # shows error_info message and stderr (but not stdout) in Shippable UI
    TestCase(name='test-case-name-error-no-\noutput', classname='class\nname', elapsed_sec=1.2, stdout='std\nout', stderr='\nstd\nerr'),
    # shows failure_info message and stderr (but not stdout) in Shippable UI
    TestCase(name='test-case-name-failure-no-\noutput', classname='class\nname', elapsed_sec=1.2, stdout='std\nout', stderr='\nstd\nerr'),
    # only counted as skipped in Shippable UI
    TestCase(name='test-case-name-skipped-no-\noutput', classname='class\nname', elapsed_sec=1.2, stdout='std\nout', stderr='\nstd\nerr'),

    # shows error_info message (empty) and error_info output (but not stdout/stderr) in Shippable UI
    TestCase(name='test-case-name-error-no-message', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    # shows failure_info message (empty) and failure_info output (but not stdout/stderr) in Shippable UI
    TestCase(name='test-case-name-failure-no-message', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),
    # only counted as skipped in Shippable UI
    TestCase(name='test-case-name-skipped-no-message', classname='classname', elapsed_sec=1.2, stdout='stdout', stderr='stderr'),

    # shows error_info message and empty stderr (but not stdout) in Shippable UI
    TestCase(name='test-case-name-error-no-stderr', classname='classname', elapsed_sec=1.2, stdout='stdout'),
    # shows failure_info message and empty stderr (but not stdout) in Shippable UI
    TestCase(name='test-case-name-failure-no-stderr', classname='classname', elapsed_sec=1.2, stdout='stdout'),
    # only counted as skipped in Shippable UI
    TestCase(name='test-case-name-skipped-no-stderr', classname='classname', elapsed_sec=1.2, stdout='stdout'),

    # optimal success
    TestCase(name='optimal-success', classname='classname'),
    # optimal error
    TestCase(name='optimal-error', classname='classname'),
    # optimal failure
    TestCase(name='optimal-failure', classname='classname'),
    # optimal skipped
    TestCase(name='optimal-skipped', classname='classname'),
]

test_cases[1].add_error_info(message='error\nmessage', output='\nerror\noutput')
test_cases[2].add_failure_info(message='failure\nmessage', output='\nfailure\noutput')
test_cases[3].add_skipped_info(message='skipped\nmessage', output='\nskipped\noutput')

test_cases[4].add_error_info(message='error message')
test_cases[5].add_failure_info(message='failure message')
test_cases[6].add_skipped_info(message='skipped message')

test_cases[7].add_error_info(output='error output')
test_cases[8].add_failure_info(output='failure output')
test_cases[9].add_skipped_info(output='skipped output')

test_cases[10].add_error_info(message='error message')
test_cases[11].add_failure_info(message='failure message')
test_cases[12].add_skipped_info(message='skipped message')

test_cases[13].add_error_info(message='optimal error message', output='\noptimal\nerror\noutput')
test_cases[14].add_failure_info(message='optimal failure message', output='\noptimal\nfailure\noutput')
test_cases[15].add_skipped_info(message='optimal skipped message', output='\noptimal\nskipped\noutput')

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
