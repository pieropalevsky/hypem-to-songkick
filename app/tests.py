from django.test import TestCase
from django.core.urlresolvers import reverse

from app.parsers import get_songkick_url, add_songkick_url

#TODO Test against fixture data, Test against API


# Views
class IndexTest(TestCase):

    def setUp(self):
        self.url = reverse('app:index')
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_form_renders(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'action="/results/"')


class ResultsTest(TestCase):
    def setUp(self):
        self.url = "%s?username=test" %reverse('app:results')
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'results.html')


class GetSongkickUrlTest(TestCase):

    def setUp(self):
        self.artist = "test artist"

    def test_get_songkick_url(self):
        expected = 'https://www.songkick.com/search?page=1&per_page=10&query=test+artist&type=artists'
        actual = get_songkick_url(self.artist)
        self.assertEqual(expected, actual)


# Parsers
class AddSongkickUrlTest(TestCase):

    def setUp(self):
        self.context = {'test artist':
                        {'count': 1}}
        self.expected_url = 'https://www.songkick.com/search?page=1&per_page=10&query=test+artist&type=artists'


    def test_add_songkick_url(self):
        expected = {'test artist':
                    {'count': 1,
                     'songkick_url': self.expected_url
                     }}
        add_songkick_url(self.context)
        self.assertEqual(expected, self.context)


