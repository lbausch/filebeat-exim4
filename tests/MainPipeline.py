import unittest
import BaseTestCase


class MainPipeline(BaseTestCase.BaseTestCase):
    pipeline_file = '../module/exim4/main/ingest/pipeline.json'

    def test_pipeline(self):
        message = 'foo'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceEqual(source, message, 'message')
        self.assertSourceEqual(source, 'Provided Grok expressions do not match field value: [foo]', 'error.message')

    def test_local_user(self):
        message = '2021-05-04 13:37:00 +0100 1fnm7Z-00DoYa-KK <= localuser@host.tld U=localuser P=local S=1512 T="Cron <localuser@host> /usr/bin/wget http://foo.tld --output-document=/h" for recipient@remotehost.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'local', 'exim4.protocol')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'localuser@host.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'localuser', 'exim4.local_user')
        self.assertSourceEqual(source, '1fnm7Z-00DoYa-KK', 'exim4.id')
        self.assertSourceEqual(source, '1512', 'exim4.message_size')
        self.assertSourceEqual(source, 'Cron <localuser@host> /usr/bin/wget http://foo.tld --output-document=/h', 'exim4.subject')
        self.assertSourceEqual(source, [
            'recipient@remotehost.tld',
        ], 'exim4.received_recipients')

    def test_authenticated_user(self):
        message = '2021-05-04 13:37:00 +0100 1fnjiM-00A4Jp-Mv <= mail@senderhost.tld H=(123.123.123.123) [124.124.124.124]:1337 P=esmtpa A=dovecot_login:mail@otherhost.tld S=7757 T="Re: [foo]" for mail@recipient.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'esmtpa', 'exim4.protocol')
        self.assertSourceEqual(source, '124.124.124.124', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_host')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'dovecot_login:mail@otherhost.tld', 'exim4.authenticator')
        self.assertSourceEqual(source, '1fnjiM-00A4Jp-Mv', 'exim4.id')
        self.assertSourceEqual(source, '7757', 'exim4.message_size')
        self.assertSourceEqual(source, 'Re: [foo]', 'exim4.subject')
        self.assertSourceEqual(source, [
            'mail@recipient.tld',
        ], 'exim4.received_recipients')

    def test_subject(self):
        message = '2021-05-04 13:37:00 +0100 1fo681-005txy-Bw <= mail@senderhost.tld H=(mail.senderhost.tld) [123.123.123.123]:1337 P=esmtpa A=dovecot_login:mail@senderhost.tld S=605 id=foobar@mail.senderhost.tld T="foobar baz" for recipient@remotehost.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'esmtpa', 'exim4.protocol')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail.senderhost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'dovecot_login:mail@senderhost.tld', 'exim4.authenticator')
        self.assertSourceEqual(source, '1fo681-005txy-Bw', 'exim4.id')
        self.assertSourceEqual(source, '605', 'exim4.message_size')
        self.assertSourceEqual(source, 'foobar@mail.senderhost.tld', 'exim4.message_id')
        self.assertSourceEqual(source, 'foobar baz', 'exim4.subject')
        self.assertSourceEqual(source, [
            'recipient@remotehost.tld',
        ], 'exim4.received_recipients')

    def test_subject_with_double_quotes(self):
        message = '2021-05-04 13:37:00 +0100 1fo681-005txy-Bw <= mail@senderhost.tld H=(mail.senderhost.tld) [123.123.123.123]:1337 P=esmtpa A=dovecot_login:mail@senderhost.tld S=605 id=foobar@mail.senderhost.tld T="foobar \\"baz \\"" for recipient@remotehost.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'esmtpa', 'exim4.protocol')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail.senderhost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'dovecot_login:mail@senderhost.tld', 'exim4.authenticator')
        self.assertSourceEqual(source, '1fo681-005txy-Bw', 'exim4.id')
        self.assertSourceEqual(source, '605', 'exim4.message_size')
        self.assertSourceEqual(source, 'foobar@mail.senderhost.tld', 'exim4.message_id')
        self.assertSourceEqual(source, 'foobar \\"baz \\"', 'exim4.subject')
        self.assertSourceEqual(source, [
            'recipient@remotehost.tld',
        ], 'exim4.received_recipients')

    def test_multiple_received_recipients(self):
        message = '2021-05-04 13:37:00 +0100 1fo6nj-005xrN-Uy <= mail@senderhost.tld H=(mail.senderhost.tld) [123.123.123.123]:1337 P=esmtpa A=dovecot_login:mail@senderhost.tld S=589 id=foobar@mail.senderhost.tld T="test" for recipient1@remotehost.tld recipient2@remotehost.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, 'esmtpa', 'exim4.protocol')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'mail.senderhost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'dovecot_login:mail@senderhost.tld', 'exim4.authenticator')
        self.assertSourceEqual(source, '1fo6nj-005xrN-Uy', 'exim4.id')
        self.assertSourceEqual(source, '589', 'exim4.message_size')
        self.assertSourceEqual(source, 'foobar@mail.senderhost.tld', 'exim4.message_id')
        self.assertSourceEqual(source, 'test', 'exim4.subject')
        self.assertSourceEqual(source, [
            'recipient1@remotehost.tld',
            'recipient2@remotehost.tld',
        ], 'exim4.received_recipients')

    def test_sender_address(self):
        message = '2021-05-04 13:37:00 +0100 1gmL1D-0004RA-NF => mail@remotehost.tld F=<mail@senderhost.tld> R=dnslookup T=remote_smtp H=mail.remotehost.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128 CV=yes DN="/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld" C="250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, '=>', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@remotehost.tld', 'exim4.final_address')
        self.assertSourceEqual(source, 'remote_smtp', 'exim4.transport')
        self.assertSourceEqual(source, '1gmL1D-0004RA-NF', 'exim4.id')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'yes', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, '250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU', 'exim4.smtp_confirmation')
        self.assertSourceEqual(source, '/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld', 'exim4.distinguished_name')

    def test_sender_address_without_smaller_than_and_greater_than(self):
        message = '2021-05-04 13:37:00 +0100 1gmL1D-0004RA-NF => mail@remotehost.tld F=mail@senderhost.tld R=dnslookup T=remote_smtp H=mail.remotehost.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128 CV=yes DN="/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld" C="250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.sender_address')
        self.assertSourceEqual(source, '=>', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@remotehost.tld', 'exim4.final_address')
        self.assertSourceEqual(source, 'remote_smtp', 'exim4.transport')
        self.assertSourceEqual(source, '1gmL1D-0004RA-NF', 'exim4.id')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'yes', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, '250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU', 'exim4.smtp_confirmation')
        self.assertSourceEqual(source, '/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld', 'exim4.distinguished_name')

    def test_dkim_parsing(self):
        message = '2021-05-04 13:37:00 +0100 1gon8g-0001rZ-K0 <= mail@senderhost.tld H=mail.remotehost.tld [123.123.123.123] P=esmtpsa X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=no A=fixed_cram:foo K S=10258521 DKIM=remotehost.tld id=foobar@mail.remotehost.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'esmtpsa', 'exim4.protocol')
        self.assertSourceEqual(source, 'K', 'exim4.chunking')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'no', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, '1gon8g-0001rZ-K0', 'exim4.id')
        self.assertSourceEqual(source, 'foobar@mail.remotehost.tld', 'exim4.message_id')
        self.assertSourceEqual(source, 'fixed_cram:foo', 'exim4.authenticator')
        self.assertSourceEqual(source, 'remotehost.tld', 'exim4.dkim')
        self.assertSourceEqual(source, '10258521', 'exim4.message_size')
        self.assertSourceEqual(source, 'K', 'exim4.chunking')

    def test_delivery_failed_address_bounced(self):
        message = '2021-05-04 13:37:00 +0100 1gpXfR-0040X2-94 ** mail@host.tld R=virtual_aliases: No Such User Here'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '**', 'exim4.flag')
        self.assertSourceEqual(source, 'virtual_aliases:', 'exim4.router')
        self.assertSourceEqual(source, 'mail@host.tld', 'exim4.final_address')
        self.assertSourceEqual(source, '1gpXfR-0040X2-94', 'exim4.id')

    def test_exim_flag_with_following_whitespaces(self):
        message = '2021-05-04 13:37:00 +0100 1gtTXl-009NOy-Ft ->  foo@bar.tld <" foo.bar"@baz.tld> R=dkim_lookuphost T=dkim_remote_smtp H=mail.host.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=yes A=fixed_cram K C="250- 4359466 byte chunk, total 4361651\\n250 OK id=1gtTZ9-0003pq-QN"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '->', 'exim4.flag')
        self.assertSourceEqual(source, 'foo@bar.tld', 'exim4.final_address')
        self.assertSourceEqual(source, '1gtTXl-009NOy-Ft', 'exim4.id')
        self.assertSourceEqual(source, 'dkim_lookuphost', 'exim4.router')
        self.assertSourceEqual(source, 'dkim_remote_smtp', 'exim4.transport')
        self.assertSourceEqual(source, 'mail.host.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'yes', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, 'fixed_cram', 'exim4.authenticator')
        self.assertSourceEqual(source, 'K', 'exim4.chunking')
        self.assertSourceEqual(source, '250- 4359466 byte chunk, total 4361651\\n250 OK id=1gtTZ9-0003pq-QN', 'exim4.smtp_confirmation')

    def test_delivery_deferred(self):
        message = "2021-05-04 13:37:00 +0100 1h43YE-0005F1-ND == mail@host.tld R=dnslookup T=remote_smtp defer (-53): retry time not reached for any host for 'host.tld'"

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '1h43YE-0005F1-ND', 'exim4.id')
        self.assertSourceEqual(source, '==', 'exim4.flag')
        self.assertSourceEqual(source, 'dnslookup', 'exim4.router')
        self.assertSourceEqual(source, 'mail@host.tld', 'exim4.final_address')
        self.assertSourceEqual(source, 'remote_smtp', 'exim4.transport')

    def test_sender_rewriting_scheme(self):
        message = '2021-05-04 13:37:00 +0100 1hEsVV-006q9f-M2 => mail@host.tld <foo@otherhost.tld> SRS=<SRS0=MQyYEB=SO=otherhost.tld=foo@otherhost.tld> R=tls_lookuphost T=tls_remote_smtp H=mail.remotehost.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=yes A=fixed_cram K C="250- 1319 byte chunk, total 1319\\n250 OK id=1hEsVX-0004tM-38"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '=>', 'exim4.flag')
        self.assertSourceEqual(source, 'foo@otherhost.tld', 'exim4.original_address')
        self.assertSourceEqual(source, 'mail@host.tld', 'exim4.final_address')
        self.assertSourceEqual(source, '1hEsVV-006q9f-M2', 'exim4.id')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '250- 1319 byte chunk, total 1319\\n250 OK id=1hEsVX-0004tM-38', 'exim4.smtp_confirmation')
        self.assertSourceEqual(source, 'tls_remote_smtp', 'exim4.transport')
        self.assertSourceEqual(source, 'mail.remotehost.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'tls_lookuphost', 'exim4.router')
        self.assertSourceEqual(source, 'SRS0=MQyYEB=SO=otherhost.tld=foo@otherhost.tld', 'exim4.srs')
        self.assertSourceEqual(source, 'K', 'exim4.chunking')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'yes', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, 'fixed_cram', 'exim4.authenticator')

    def test_sender_rewriting_scheme_as_original_address(self):
        message = '2021-05-04 13:37:00 +0100 1hEsuk-00027r-A0 => sender@somehost.tld <SRS0=dRnd8e=SO=mail.host.tld=foo@bar.tld> F=<> R=dnslookup T=remote_smtp H=mail.host.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=yes DN="/C=CH/ST=foo/L=bar/O=baz/OU=foobar/CN=mail.host.tld" C="250 2.0.0 Ok: queued as 44gYF23FjFzsHn52"'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '=>', 'exim4.flag')
        self.assertSourceEqual(source, 'SRS0=dRnd8e=SO=mail.host.tld=foo@bar.tld', 'exim4.original_address')
        self.assertSourceEqual(source, 'sender@somehost.tld', 'exim4.final_address')
        self.assertSourceEqual(source, '', 'exim4.sender_address')
        self.assertSourceEqual(source, '1hEsuk-00027r-A0', 'exim4.id')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '250 2.0.0 Ok: queued as 44gYF23FjFzsHn52', 'exim4.smtp_confirmation')
        self.assertSourceEqual(source, 'remote_smtp', 'exim4.transport')
        self.assertSourceEqual(source, 'mail.host.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'dnslookup', 'exim4.router')
        self.assertSourceEqual(source, 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'yes', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, '/C=CH/ST=foo/L=bar/O=baz/OU=foobar/CN=mail.host.tld', 'exim4.distinguished_name')

    def test_empty_remote_host(self):
        message = '2021-05-04 13:37:00 +0100 1hgCb6-0003NE-Ka <= mail@senderhost.tld H=([]) [123.123.123.123]:1337 P=esmtpsa X=TLSv1:ECDHE-RSA-AES128-SHA:128 CV=no A=dovecot_plain:foobar@mail.host.tld S=233358 id=foobar@mail.host.tld T="baz" for mail@recipient.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '1hgCb6-0003NE-Ka', 'exim4.id')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'mail@senderhost.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, 'esmtpsa', 'exim4.protocol')
        self.assertSourceEqual(source, 'TLSv1:ECDHE-RSA-AES128-SHA:128', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'no', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, 'dovecot_plain:foobar@mail.host.tld', 'exim4.authenticator')
        self.assertSourceEqual(source, '233358', 'exim4.message_size')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'foobar@mail.host.tld', 'exim4.message_id')
        self.assertSourceEqual(source, 'baz', 'exim4.subject')
        self.assertSourceEqual(source, [
            'mail@recipient.tld',
        ], 'exim4.received_recipients')

    def test_helo_name_with_square_brackets(self):
        message = '2021-05-04 13:37:00 +0100 1hF34W-00A7sG-0U <= sender@host.tld H=mail.host.tld ([mail.host.tld]) [123.123.123.123]:1337 P=esmtpsa X=TLSv1:ECDHE-RSA-AES256-SHA:256 CV=no A=dovecot_plain:sender@host.tld S=238248 id=foo@bar.tld T="test" for recipient@otherhost.tld'

        response = self.request(message)

        source = self.source(response)

        self.assertSourceHasNoError(source)
        self.assertSourceEqual(source, message, 'exim4.message_raw')
        self.assertSourceEqual(source, '2021-05-04T13:37:00.000+01:00', '@timestamp')
        self.assertSourceEqual(source, '1hF34W-00A7sG-0U', 'exim4.id')
        self.assertSourceEqual(source, '<=', 'exim4.flag')
        self.assertSourceEqual(source, 'sender@host.tld', 'exim4.envelope_sender')
        self.assertSourceEqual(source, 'mail.host.tld', 'exim4.remote_host')
        self.assertSourceEqual(source, 'mail.host.tld', 'exim4.helo_name')
        self.assertSourceEqual(source, '123.123.123.123', 'exim4.remote_addr')
        self.assertSourceEqual(source, '1337', 'exim4.remote_addr_port')
        self.assertSourceEqual(source, 'esmtpsa', 'exim4.protocol')
        self.assertSourceEqual(source, 'TLSv1:ECDHE-RSA-AES256-SHA:256', 'exim4.tls.cipher_suite')
        self.assertSourceEqual(source, 'no', 'exim4.tls.cert_verification_status')
        self.assertSourceEqual(source, 'dovecot_plain:sender@host.tld', 'exim4.authenticator')
        self.assertSourceEqual(source, '238248', 'exim4.message_size')
        self.assertSourceEqual(source, 'foo@bar.tld', 'exim4.message_id')
        self.assertSourceEqual(source, 'test', 'exim4.subject')
        self.assertSourceEqual(source, [
            'recipient@otherhost.tld',
        ], 'exim4.received_recipients')


if __name__ == '__main__':
    unittest.main()
