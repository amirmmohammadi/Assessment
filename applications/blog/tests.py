from django.urls import reverse
from rest_framework import status

from applications.common.tests import BaseAPITestCase, fake
from .models import Content, ContentScore


class ListContentAPIViewTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()

        self.content1 = Content.objects.create(title=fake.sentence(), body=fake.text(), owner=self.user)
        self.content2 = Content.objects.create(title=fake.sentence(), body=fake.text(), owner=self.user)

        ContentScore.objects.create(content=self.content1, owner=self.user, score=5)
        ContentScore.objects.create(content=self.content2, owner=self.user, score=2)

    def test_list_content(self):
        response = self.client.get(reverse('blog-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content_data = response.data['results']
        self.assertEqual(len(content_data), 2)

        for content in content_data:
            self.assertIn('user_score', content)
            self.assertIsNotNone(content['user_score'])

            self.assertIn('title', content)
            self.assertIn('body', content)


class SubmitScoreAPIViewTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.content = Content.objects.create(title=fake.sentence(), body=fake.text(), owner=self.user)

    def test_submit_score_create(self):
        score = 3
        data = {
            'content': self.content.id,
            'score': score
        }

        response = self.client.post(reverse('submit-score'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Score created successfully.")

    def test_submit_score_update(self):
        old_score = 2
        new_score = 3
        ContentScore.objects.create(content=self.content, owner=self.user, score=old_score)

        data = {
            'content': self.content.id,
            'score': new_score
        }

        response = self.client.post(reverse('submit-score'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Score updated successfully.")

        content_score = ContentScore.objects.get(content=self.content, owner=self.user)
        self.assertEqual(content_score.score, score)

    def test_submit_score_update_validation_error(self):
        score = 9
        ContentScore.objects.create(content=self.content, owner=self.user, score=score)

        data = {
            'content': self.content.id,
            'score': score
        }

        response = self.client.post(reverse('submit-score'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        content_score = ContentScore.objects.get(content=self.content, owner=self.user)
        self.assertEqual(content_score.score, score)
