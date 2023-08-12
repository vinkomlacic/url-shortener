from unittest.mock import patch

from django.test import TestCase

from accounts.models import User


class CoreModelsTest(TestCase):

    @patch('core.models.random.choice')
    def test_url_mapping_generate_short_url(self, choice):
        # The following configuration of the mock makes sure that the random
        # generation of the short URL returns the following three values
        # consequently:
        #   1. aaaaaaaaaa
        #   2. aaaaaaaaaa
        #   3. bbbbbbbbbb
        short_url_length = 10
        choice.side_effect = (short_url_length * 2) * ['a'] + \
                             (short_url_length * ['b'])

        user = User.objects.create_user(username='test', password='password')
        url_mapping_1 = user.url_mappings.create(url='https://example.org')
        self.assertEqual(url_mapping_1.short_url, 'a' * short_url_length)

        # Creation of this URL mapping should cause the generation algorithm
        # to cycle two times in order to find a unique short URL. The first
        # time the collision is encountered, and the second time, a truly
        # unique short URL is found.
        url_mapping_2 = user.url_mappings.create(url='https://example.org')
        self.assertEqual(url_mapping_2.short_url, 'b' * short_url_length)

        # For each round of generation the choice is called short_url_length
        # times. There were three round: 1st with the url_mapping_1, 2nd with
        # the url_mapping_2 (collision), and the 3rd with the url_mapping_2
        # where the unique short URL was finally found
        self.assertEqual(choice.call_count, 3 * short_url_length)
