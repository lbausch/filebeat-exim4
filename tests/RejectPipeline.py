import unittest
import BaseTestCase


class RejectPipeline(BaseTestCase.BaseTestCase):
    pipeline_file = '../module/exim4/reject/ingest/pipeline.json'

    def test_pipeline(self):
        message = 'foo'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            'message': message,
            'error': {
                'message': 'Provided Grok expressions do not match field value: [foo]'
            }
        })

    def test_exim497_message_id_format(self):
        message = '2024-06-02 05:50:20 +0200 1sDcEe-000000004BC-0oYZ H=example.com [127.0.0.1] X=TLS1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=no F=<sender@example.com> A=fixed_cram:foo rejected after DATA: spam'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2024-06-02T05:50:20.000+02:00',
            'exim4': {
                'message_raw': message,
                'id': '1sDcEe-000000004BC-0oYZ',
                'remote_host': 'example.com',
                'remote_addr': '127.0.0.1',
                'tls': {
                    'cert_verification_status': 'no',
                    'cipher_suite': 'TLS1.2:ECDHE-RSA-AES256-GCM-SHA384:256'
                },
                'sender_address': 'sender@example.com',
                'authenticator':  'fixed_cram:foo',
                'message': 'rejected after DATA: spam',
            },
        })

    def test_greylisting(self):
        message = "2021-05-04 13:37:00 +0100 H=mail.remotehost.tld [123.123.123.123]:1337 X=TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128 CV=no F=<mail@sender.tld> temporarily rejected RCPT <mail@recipient.tld>: Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'none'"

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_host': 'mail.remotehost.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128',
                    'cert_verification_status': 'no',
                },
                'sender_address': 'mail@sender.tld',
                'recipient_address': 'mail@recipient.tld',
                'message': "Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'none'",
            },
        })

    def test_greylisting_without_cipher_suite(self):
        message = "2021-05-04 13:37:00 +0100 H=(mail.remotehost.tld) [123.123.123.123]:1337 F=<mail@sender.tld> temporarily rejected RCPT <mail@recipient.tld>: Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'neutral'"

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_host': 'mail.remotehost.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'sender_address': 'mail@sender.tld',
                'recipient_address': 'mail@recipient.tld',
                'message': "Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'neutral'",
            },
        })


    def test_rbl(self):
        message = '2021-05-04 13:37:00 +0100 H=(mail.remotehost.tld) [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: "JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see [https://rbl.tld]"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_host': 'mail.remotehost.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'sender_address': 'mail@sender.tld',
                'recipient_address': 'mail@recipient.tld',
                'message': '"JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see [https://rbl.tld]"',
            },
        })

    def test_spf(self):
        message = '2021-05-04 13:37:00 +0100 H=mail.remotehost.tld [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: SPF: 123.123.123.123 is not allowed to send mail from sender.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_host': 'mail.remotehost.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'sender_address': 'mail@sender.tld',
                'recipient_address': 'mail@recipient.tld',
                'message': 'SPF: 123.123.123.123 is not allowed to send mail from sender.tld',
            },
        })

    def test_no_such_user_here(self):
        message = '2021-05-04 13:37:00 +0100 H=mail.remotehost.tld [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: No Such User Here"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_host': 'mail.remotehost.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'sender_address': 'mail@sender.tld',
                'recipient_address': 'mail@recipient.tld',
                'message': 'No Such User Here"',
            },
        })


    def test_rejected_junk_mail(self):
        message = '2021-05-04 13:37:00 +0100 H=(mail.remotehost.tld) [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: "JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see https://rbl.tld"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_host': 'mail.remotehost.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'sender_address': 'mail@sender.tld',
                'recipient_address': 'mail@recipient.tld',
                'message': '"JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see https://rbl.tld"',
            },
        })

    def test_dropped_syntax_errors(self):
        message = '2021-05-04 13:37:00 +0100 SMTP call from (mail.remotehost.tld) [123.123.123.123]:1337 dropped: too many syntax or protocol errors (last command was "RCPT TO: <\'mail@recipient.tld\'>",  C=EHLO,AUTH,MAIL,RCPT,RCPT,RCPT,RCPT,RCPT,RCPT)'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'message': 'SMTP call from (mail.remotehost.tld) [123.123.123.123]:1337 dropped: too many syntax or protocol errors (last command was "RCPT TO: <\'mail@recipient.tld\'>",  C=EHLO,AUTH,MAIL,RCPT,RCPT,RCPT,RCPT,RCPT,RCPT)',
            },
        })


if __name__ == '__main__':
    unittest.main()
