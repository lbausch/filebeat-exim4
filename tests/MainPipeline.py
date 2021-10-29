import unittest
import BaseTestCase


class MainPipeline(BaseTestCase.BaseTestCase):
    pipeline_file = '../module/exim4/main/ingest/pipeline.json'

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

    def test_local_user(self):
        message = '2021-05-04 13:37:00 +0100 1fnm7Z-00DoYa-KK <= localuser@host.tld U=localuser P=local S=1512 T="Cron <localuser@host> /usr/bin/wget http://foo.tld --output-document=/h" for recipient@remotehost.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'protocol': 'local',
                'flag': '<=',
                'envelope_sender': 'localuser@host.tld',
                'local_user': 'localuser',
                'id': '1fnm7Z-00DoYa-KK',
                'message_size': '1512',
                'subject': 'Cron <localuser@host> /usr/bin/wget http://foo.tld --output-document=/h',
                'received_recipients': [
                    'recipient@remotehost.tld',
                ],
            },
        })

    def test_authenticated_user(self):
        message = '2021-05-04 13:37:00 +0100 1fnjiM-00A4Jp-Mv <= mail@senderhost.tld H=(123.123.123.123) [124.124.124.124]:1337 P=esmtpa A=dovecot_login:mail@otherhost.tld S=7757 T="Re: [foo]" for mail@recipient.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'protocol': 'esmtpa',
                'remote_addr': '124.124.124.124',
                'remote_addr_port': '1337',
                'remote_host': '123.123.123.123',
                'flag': '<=',
                'envelope_sender': 'mail@senderhost.tld',
                'authenticator': 'dovecot_login:mail@otherhost.tld',
                'id': '1fnjiM-00A4Jp-Mv',
                'message_size': '7757',
                'subject': 'Re: [foo]',
                'received_recipients': [
                    'mail@recipient.tld',
                ],
            },
        })

    def test_subject(self):
        message = '2021-05-04 13:37:00 +0100 1fo681-005txy-Bw <= mail@senderhost.tld H=(mail.senderhost.tld) [123.123.123.123]:1337 P=esmtpa A=dovecot_login:mail@senderhost.tld S=605 id=foobar@mail.senderhost.tld T="foobar baz" for recipient@remotehost.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'protocol': 'esmtpa',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'remote_host': 'mail.senderhost.tld',
                'flag': '<=',
                'envelope_sender': 'mail@senderhost.tld',
                'authenticator': 'dovecot_login:mail@senderhost.tld',
                'id': '1fo681-005txy-Bw',
                'message_size': '605',
                'message_id': 'foobar@mail.senderhost.tld',
                'subject': 'foobar baz',
                'received_recipients': [
                    'recipient@remotehost.tld',
                ],
            },
        })

    def test_subject_with_double_quotes(self):
        message = '2021-05-04 13:37:00 +0100 1fo681-005txy-Bw <= mail@senderhost.tld H=(mail.senderhost.tld) [123.123.123.123]:1337 P=esmtpa A=dovecot_login:mail@senderhost.tld S=605 id=foobar@mail.senderhost.tld T="foobar \\"baz \\"" for recipient@remotehost.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'protocol': 'esmtpa',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'remote_host': 'mail.senderhost.tld',
                'flag': '<=',
                'envelope_sender': 'mail@senderhost.tld',
                'authenticator': 'dovecot_login:mail@senderhost.tld',
                'id': '1fo681-005txy-Bw',
                'message_size': '605',
                'message_id': 'foobar@mail.senderhost.tld',
                'subject': 'foobar \\"baz \\"',
                'received_recipients': [
                    'recipient@remotehost.tld',
                ],
            },
        })

    def test_multiple_received_recipients(self):
        message = '2021-05-04 13:37:00 +0100 1fo6nj-005xrN-Uy <= mail@senderhost.tld H=(mail.senderhost.tld) [123.123.123.123]:1337 P=esmtpa A=dovecot_login:mail@senderhost.tld S=589 id=foobar@mail.senderhost.tld T="test" for recipient1@remotehost.tld recipient2@remotehost.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'protocol': 'esmtpa',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'remote_host': 'mail.senderhost.tld',
                'flag': '<=',
                'envelope_sender': 'mail@senderhost.tld',
                'authenticator': 'dovecot_login:mail@senderhost.tld',
                'id': '1fo6nj-005xrN-Uy',
                'message_size': '589',
                'message_id': 'foobar@mail.senderhost.tld',
                'subject': 'test',
                'received_recipients': [
                    'recipient1@remotehost.tld',
                    'recipient2@remotehost.tld',
                ]
            },
        })

    def test_sender_address(self):
        message = '2021-05-04 13:37:00 +0100 1gmL1D-0004RA-NF => mail@remotehost.tld F=<mail@senderhost.tld> R=dnslookup T=remote_smtp H=mail.remotehost.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128 CV=yes DN="/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld" C="250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_addr': '123.123.123.123',
                'sender_address': 'mail@senderhost.tld',
                'flag': '=>',
                'final_address': 'mail@remotehost.tld',
                'transport': 'remote_smtp',
                'id': '1gmL1D-0004RA-NF',
                'remote_host': 'mail.remotehost.tld',
                'router': 'dnslookup',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128',
                    'cert_verification_status': 'yes',
                },
                'smtp_confirmation': '250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU',
                'distinguished_name': '/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld',
            },
        })

    def test_sender_address_without_smaller_than_and_greater_than(self):
        message = '2021-05-04 13:37:00 +0100 1gmL1D-0004RA-NF => mail@remotehost.tld F=mail@senderhost.tld R=dnslookup T=remote_smtp H=mail.remotehost.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128 CV=yes DN="/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld" C="250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_addr': '123.123.123.123',
                'sender_address': 'mail@senderhost.tld',
                'flag': '=>',
                'final_address': 'mail@remotehost.tld',
                'transport': 'remote_smtp',
                'id': '1gmL1D-0004RA-NF',
                'remote_host': 'mail.remotehost.tld',
                'router': 'dnslookup',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES128-GCM-SHA256:128',
                    'cert_verification_status': 'yes',
                },
                'smtp_confirmation': '250 Requested mail action okay, completed: id=1MCJaS-1gviwC0ZZS-009SFU',
                'distinguished_name': '/C=DE/O=foo/ST=bar/L=baz/CN=mail.remotehost.tld',
            },
        })

    def test_dkim_parsing(self):
        message = '2021-05-04 13:37:00 +0100 1gon8g-0001rZ-K0 <= mail@senderhost.tld H=mail.remotehost.tld [123.123.123.123] P=esmtpsa X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=no A=fixed_cram:foo K S=10258521 DKIM=remotehost.tld id=foobar@mail.remotehost.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_addr': '123.123.123.123',
                'flag': '<=',
                'envelope_sender': 'mail@senderhost.tld',
                'remote_host': 'mail.remotehost.tld',
                'protocol': 'esmtpsa',
                'chunking': 'K',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256',
                    'cert_verification_status': 'no',
                },
                'id': '1gon8g-0001rZ-K0',
                'message_id': 'foobar@mail.remotehost.tld',
                'authenticator': 'fixed_cram:foo',
                'dkim': 'remotehost.tld',
                'message_size': '10258521',
            },
        })

    def test_delivery_failed_address_bounced(self):
        message = '2021-05-04 13:37:00 +0100 1gpXfR-0040X2-94 ** mail@host.tld R=virtual_aliases: No Such User Here'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'flag': '**',
                'router': 'virtual_aliases:',
                'final_address': 'mail@host.tld',
                'id': '1gpXfR-0040X2-94',
            },
        })

    def test_exim_flag_with_following_whitespaces(self):
        message = '2021-05-04 13:37:00 +0100 1gtTXl-009NOy-Ft ->  foo@bar.tld <" foo.bar"@baz.tld> R=dkim_lookuphost T=dkim_remote_smtp H=mail.host.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=yes A=fixed_cram K C="250- 4359466 byte chunk, total 4361651\\n250 OK id=1gtTZ9-0003pq-QN"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'remote_addr': '123.123.123.123',
                'flag': '->',
                'final_address': 'foo@bar.tld',
                'id': '1gtTXl-009NOy-Ft',
                'original_address_malformed': '" foo.bar"@baz.tld',
                'router': 'dkim_lookuphost',
                'transport': 'dkim_remote_smtp',
                'remote_host': 'mail.host.tld',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256',
                    'cert_verification_status': 'yes',
                },
                'authenticator': 'fixed_cram',
                'chunking': 'K',
                'smtp_confirmation': '250- 4359466 byte chunk, total 4361651\\n250 OK id=1gtTZ9-0003pq-QN',
            },
        })

    def test_delivery_deferred(self):
        message = "2021-05-04 13:37:00 +0100 1h43YE-0005F1-ND == mail@host.tld R=dnslookup T=remote_smtp defer (-53): retry time not reached for any host for 'host.tld'"

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'id': '1h43YE-0005F1-ND',
                'flag': '==',
                'router': 'dnslookup',
                'final_address': 'mail@host.tld',
                'transport': 'remote_smtp',
            },
        })

    def test_sender_rewriting_scheme(self):
        message = '2021-05-04 13:37:00 +0100 1hEsVV-006q9f-M2 => mail@host.tld <foo@otherhost.tld> SRS=<SRS0=MQyYEB=SO=otherhost.tld=foo@otherhost.tld> R=tls_lookuphost T=tls_remote_smtp H=mail.remotehost.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=yes A=fixed_cram K C="250- 1319 byte chunk, total 1319\\n250 OK id=1hEsVX-0004tM-38"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'flag': '=>',
                'original_address': 'foo@otherhost.tld',
                'final_address': 'mail@host.tld',
                'id': '1hEsVV-006q9f-M2',
                'remote_addr': '123.123.123.123',
                'smtp_confirmation': '250- 1319 byte chunk, total 1319\\n250 OK id=1hEsVX-0004tM-38',
                'transport': 'tls_remote_smtp',
                'remote_host': 'mail.remotehost.tld',
                'router': 'tls_lookuphost',
                'srs': 'SRS0=MQyYEB=SO=otherhost.tld=foo@otherhost.tld',
                'chunking': 'K',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256',
                    'cert_verification_status': 'yes',
                },
                'authenticator': 'fixed_cram',
            },
        })

    def test_sender_rewriting_scheme_as_original_address(self):
        message = '2021-05-04 13:37:00 +0100 1hEsuk-00027r-A0 => sender@somehost.tld <SRS0=dRnd8e=SO=mail.host.tld=foo@bar.tld> F=<> R=dnslookup T=remote_smtp H=mail.host.tld [123.123.123.123] X=TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256 CV=yes DN="/C=CH/ST=foo/L=bar/O=baz/OU=foobar/CN=mail.host.tld" C="250 2.0.0 Ok: queued as 44gYF23FjFzsHn52"'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'flag': '=>',
                'original_address': 'SRS0=dRnd8e=SO=mail.host.tld=foo@bar.tld',
                'final_address': 'sender@somehost.tld',
                'sender_address': '',
                'id': '1hEsuk-00027r-A0',
                'remote_addr': '123.123.123.123',
                'smtp_confirmation': '250 2.0.0 Ok: queued as 44gYF23FjFzsHn52',
                'transport': 'remote_smtp',
                'remote_host': 'mail.host.tld',
                'router': 'dnslookup',
                'tls': {
                    'cipher_suite': 'TLSv1.2:ECDHE-RSA-AES256-GCM-SHA384:256',
                    'cert_verification_status': 'yes',
                },
                'distinguished_name': '/C=CH/ST=foo/L=bar/O=baz/OU=foobar/CN=mail.host.tld',
            },
        })

    def test_empty_remote_host(self):
        message = '2021-05-04 13:37:00 +0100 1hgCb6-0003NE-Ka <= mail@senderhost.tld H=([]) [123.123.123.123]:1337 P=esmtpsa X=TLSv1:ECDHE-RSA-AES128-SHA:128 CV=no A=dovecot_plain:foobar@mail.host.tld S=233358 id=foobar@mail.host.tld T="baz" for mail@recipient.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'id': '1hgCb6-0003NE-Ka',
                'flag': '<=',
                'envelope_sender': 'mail@senderhost.tld',
                'remote_addr': '123.123.123.123',
                'protocol': 'esmtpsa',
                'tls': {
                    'cipher_suite': 'TLSv1:ECDHE-RSA-AES128-SHA:128',
                    'cert_verification_status': 'no',
                },
                'authenticator': 'dovecot_plain:foobar@mail.host.tld',
                'message_size': '233358',
                'remote_addr_port': '1337',
                'message_id': 'foobar@mail.host.tld',
                'subject': 'baz',
                'received_recipients': [
                    'mail@recipient.tld',
                ],
            },
        })

    def test_helo_name_with_square_brackets(self):
        message = '2021-05-04 13:37:00 +0100 1hF34W-00A7sG-0U <= sender@host.tld H=mail.host.tld ([mail.host.tld]) [123.123.123.123]:1337 P=esmtpsa X=TLSv1:ECDHE-RSA-AES256-SHA:256 CV=no A=dovecot_plain:sender@host.tld S=238248 id=foo@bar.tld T="test" for recipient@otherhost.tld'

        response = self.request(message)
        source = self.source(response)

        self.assertSourceEquals(source, {
            '@timestamp': '2021-05-04T13:37:00.000+01:00',
            'exim4': {
                'message_raw': message,
                'id': '1hF34W-00A7sG-0U',
                'flag': '<=',
                'envelope_sender': 'sender@host.tld',
                'remote_host': 'mail.host.tld',
                'helo_name': 'mail.host.tld',
                'remote_addr': '123.123.123.123',
                'remote_addr_port': '1337',
                'protocol': 'esmtpsa',
                'tls': {
                    'cipher_suite': 'TLSv1:ECDHE-RSA-AES256-SHA:256',
                    'cert_verification_status': 'no',
                },
                'authenticator': 'dovecot_plain:sender@host.tld',
                'message_size': '238248',
                'message_id': 'foo@bar.tld',
                'subject': 'test',
                'received_recipients': [
                    'recipient@otherhost.tld',
                ],
            },
        })


if __name__ == '__main__':
    unittest.main()
