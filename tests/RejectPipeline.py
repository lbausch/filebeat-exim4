import unittest
import BaseTestCase


class RejectPipeline(BaseTestCase.BaseTestCase):
    pipeline_file = '../module/exim4/reject/ingest/pipeline.json'

    def test_pipeline(self):
        message = 'foo'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceEqual(source, message, 'message')
        self.assertSourceEqual(source, 'Provided Grok expressions do not match field value: [foo]', 'error.message')

    def test_greylisting(self):
        message = "2021-05-04 13:37:00 +0100 H=mail.remotehost.tld [123.123.123.123]:1337 X=TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128 CV=no F=<mail@sender.tld> temporarily rejected RCPT <mail@recipient.tld>: Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'none'"

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'no', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, 'mail@sender.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, 'mail@recipient.tld', 'exim4.recipient_address')
        self.assertSourceEqual(source, "Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'none'", 'exim4.message')

    def test_greylisting_without_cipher_suite(self):
        message = "2021-05-04 13:37:00 +0100 H=(mail.remotehost.tld) [123.123.123.123]:1337 F=<mail@sender.tld> temporarily rejected RCPT <mail@recipient.tld>: Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'neutral'"

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail@sender.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, 'mail@recipient.tld', 'exim4.recipient_address')
        self.assertSourceEqual(source, "Deferred due to greylisting. Host: '123.123.123.123' From: 'mail@sender.tld' To: 'mail@recipient.tld' SPF: 'neutral'", 'exim4.message')

    def test_rbl(self):
        message = '2021-05-04 13:37:00 +0100 H=(mail.remotehost.tld) [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: "JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see [https://rbl.tld]"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail@sender.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, 'mail@recipient.tld', 'exim4.recipient_address')
        self.assertSourceEqual(source, '"JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see [https://rbl.tld]"', 'exim4.message')

    def test_spf(self):
        message = '2021-05-04 13:37:00 +0100 H=mail.remotehost.tld [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: SPF: 123.123.123.123 is not allowed to send mail from sender.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail@sender.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, 'mail@recipient.tld', 'exim4.recipient_address')
        self.assertSourceEqual(source, 'SPF: 123.123.123.123 is not allowed to send mail from sender.tld', 'exim4.message')

    def test_no_such_user_here(self):
        message = '2021-05-04 13:37:00 +0100 H=mail.remotehost.tld [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: No Such User Here"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail@sender.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, 'mail@recipient.tld', 'exim4.recipient_address')
        self.assertSourceEqual(source, 'No Such User Here"', 'exim4.message')

    def test_rejected_junk_mail(self):
        message = '2021-05-04 13:37:00 +0100 H=(mail.remotehost.tld) [123.123.123.123]:1337 F=<mail@sender.tld> rejected RCPT <mail@recipient.tld>: "JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see https://rbl.tld"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail@sender.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, 'mail@recipient.tld', 'exim4.recipient_address')
        self.assertSourceEqual(source, '"JunkMail rejected - (mail.remotehost.tld) [123.123.123.123]:1337 is in an RBL (rbl.tld), see https://rbl.tld"', 'exim4.message')

    def test_dropped_syntax_errors(self):
        message = '2021-05-04 13:37:00 +0100 SMTP call from (mail.remotehost.tld) [123.123.123.123]:1337 dropped: too many syntax or protocol errors (last command was "RCPT TO: <\'mail@recipient.tld\'>",  C=EHLO,AUTH,MAIL,RCPT,RCPT,RCPT,RCPT,RCPT,RCPT)'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'SMTP call from (mail.remotehost.tld) [123.123.123.123]:1337 dropped: too many syntax or protocol errors (last command was "RCPT TO: <\'mail@recipient.tld\'>",  C=EHLO,AUTH,MAIL,RCPT,RCPT,RCPT,RCPT,RCPT,RCPT)', 'exim4.message')


if __name__ == '__main__':
    unittest.main()
