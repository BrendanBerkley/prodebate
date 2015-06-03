from django.test import TestCase
from .models import *
from .sample_data import SampleData

# Create your tests here.

# Thanks, http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/
class PollsViewsTestCase(TestCase):

    def test_index(self):
        sample_data = SampleData()
        sample_data.create_basics()

        position_queryset_count = Position.objects.count()

        resp = self.client.get('/positions/')
        # print resp.context
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('positions' in resp.context)
        
        position_response_count = resp.context['positions'].count()
        self.assertEqual(
            position_response_count, position_queryset_count
        )