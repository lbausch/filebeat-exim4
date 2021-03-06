import json
import unittest
import os
from urllib import request
from deepdiff import DeepDiff


class BaseTestCase(unittest.TestCase):

    @property
    def pipeline_file(self):
        pass

    def assertSourceEquals(self, source: dict, expected_source: dict):
        diff = DeepDiff(source, expected_source)

        if diff != {}:
            print(diff.pretty())

        self.assertEqual(diff, {})

    def read_pipeline_file(self) -> dict:
        with open(self.pipeline_file, 'r') as file:
            pipeline_raw = file.read()

        pipeline = json.loads(pipeline_raw)

        return pipeline

    def request(self, message: str) -> str:
        pipeline = self.read_pipeline_file()

        body = {
          'pipeline': pipeline,
          'docs': [
            {
                '_index': 'index',
                '_type': '_doc',
                '_id': 'id',
                '_source': {
                    'message': message,
                },
            },
          ],
        }

        data = json.dumps(body)

        req = request.Request(
            '%s/_ingest/pipeline/_simulate' % os.getenv('ES_HOST', 'http://localhost:9200'),
            data=data.encode('utf-8'),
            method='POST',
            headers={
                'Content-Type': 'application/json',
            }
        )

        with request.urlopen(req) as response_raw:
            response = response_raw.read().decode('utf-8')

        self.assertGreater(len(response), 0)

        return response

    def source(self, response: str) -> dict:
        data = json.loads(response)

        self.assertIn('docs', data)

        docs = data.get('docs')

        self.assertEqual(len(docs), 1)

        doc_data = docs[0]

        self.assertIn('doc', doc_data)

        doc = doc_data.get('doc')

        self.assertIn('_source', doc)

        source = doc.get('_source')

        return source
