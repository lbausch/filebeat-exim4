import unittest
import BaseTestCase

class RejectPipeline(BaseTestCase.BaseTestCase):
    pipeline_file = '../module/exim4/reject/ingest/pipeline.json'

    def test_pipeline(self):
        message = 'foo'

        response = self.request(message)

        source = self.source(response)

        self.assertEqual(message, source.get('message'))

if __name__ == '__main__':
    unittest.main()
