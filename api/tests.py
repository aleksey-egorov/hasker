import requests
import json
import re
from django.test import TestCase
from django.conf import settings

# Create your tests here.

class ApiIndexTestCase(TestCase):
    token = ''

    def get_api_response(self, path):
        if self.token == '':
            uri = 'http://' + settings.SITE_URL + '/api-token-auth/'
            resp = requests.post(uri, data={"username": "alex1", "password": "123"})
            resp_json = json.loads(resp.text)
            self.token = resp_json['token']

        headers = {"Authorization": "JWT " + self.token}
        uri = 'http://' + settings.SITE_URL + '/api/' + path
        resp = requests.get(uri, headers=headers)
        resp_json = json.loads(resp.text)
        return resp.status_code, resp_json

    def test_index(self):
        status_code, resp = self.get_api_response('v1/index/')
        self.assertEqual(status_code, 200)
        self.assertGreater(resp['count'], 0)
        self.assertGreater(resp['results'][0]['id'], 0)
        self.assertGreater(len(resp['results'][0]['heading']), 0)

    def test_trending(self):
        status_code, resp = self.get_api_response('v1/trending/')
        self.assertEqual(status_code, 200)
        self.assertGreater(resp['count'], 0)
        self.assertGreater(resp['results'][0]['id'], 0)
        self.assertGreaterEqual(resp['results'][0]['votes'], resp['results'][-1]['votes'])

    def test_search(self):
        status_code, resp = self.get_api_response('v1/search/?q=python')
        self.assertEqual(status_code, 200)
        self.assertGreater(resp['count'], 0)
        self.assertGreater(resp['results'][0]['id'], 0)
        regex = re.compile("python", re.IGNORECASE)
        self.assertRegex(resp["results"][0]['heading'], regex)

    def test_question(self):
        status_code, resp = self.get_api_response('v1/questions/1/')
        self.assertEqual(status_code, 200)
        self.assertEqual(resp['id'], 1)
        self.assertGreater(len(resp['heading']), 0)
        self.assertGreater(len(resp['content']), 0)

    def test_answers(self):
        status_code, resp = self.get_api_response('v1/questions/1/answers/')
        self.assertEqual(status_code, 200)
        self.assertGreater(len(resp), 0)
        self.assertGreater(resp[0]['id'], 0)
