from django.test import TestCase
from django.core.urlresolvers import reverse


class APIViewTests(TestCase):
    def test_api_get(self):
        """If api is called, must return a user and tweets."""
        response = self.client.get(reverse('twitter_data'), kwargs={'picture_toggle': 'all', 'retweet_count': 'all'})
        self.assertEqual(response.status_code, 200)
        print response
        print response.context['user']
        self.assertTrue(response.context['user'])
