import datetime
import re
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from user.models import User
from question.models import Question, Answer

# Create your tests here.

class ApiIndexTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='test')
        self.question = Question.objects.create(heading='Question about Python', pub_date=datetime.datetime.now(), votes=2, author=self.user)
        Question.objects.create(heading='Question about Go', pub_date=datetime.datetime.now(), votes=4, author=self.user)
        Question.objects.create(heading='Question about Nginx', pub_date=datetime.datetime.now(), votes=1, author=self.user)
        Question.objects.create(heading='Question about Ubuntu', pub_date=datetime.datetime.now(), votes=5, author=self.user)
        Question.objects.create(heading='Question about SQL', pub_date=datetime.datetime.now(), votes=3, author=self.user)
        Answer.objects.create(content='Answer 1', pub_date=datetime.datetime.now(), question_ref=self.question, author=self.user)
        Answer.objects.create(content='Answer 2', pub_date=datetime.datetime.now(), question_ref=self.question, author=self.user)
        Answer.objects.create(content='Answer 3', pub_date=datetime.datetime.now(), question_ref=self.question, author=self.user)

        self.client = APIClient(enforce_csrf_checks=True)


    def test_index(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get('/api/v1/index/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resp.json()['count'],
            Question.objects.count())

    def test_trending(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get('/api/v1/trending/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resp.json()['count'],
            Question.objects.count())
        votes = [result['votes'] for result in resp.json()['results']]
        self.assertEqual([5, 4, 3, 2, 1], votes)

    def stest_search(self):
        status_code, resp = self.get_api_response('v1/search/?q=python')
        self.assertEqual(status_code, 200)
        self.assertGreater(resp['count'], 0)
        self.assertGreater(resp['results'][0]['id'], 0)
        regex = re.compile("python", re.IGNORECASE)
        self.assertRegex(resp["results"][0]['heading'], regex)

    def stest_question(self):
        status_code, resp = self.get_api_response('v1/questions/1/')
        self.assertEqual(status_code, 200)
        self.assertEqual(resp['id'], 1)
        self.assertGreater(len(resp['heading']), 0)
        self.assertGreater(len(resp['content']), 0)

    def stest_answers(self):
        status_code, resp = self.get_api_response('v1/questions/1/answers/')
        self.assertEqual(status_code, 200)
        self.assertGreater(len(resp), 0)
        self.assertGreater(resp[0]['id'], 0)
