from django.core.management.base import BaseCommand, CommandError
from pro_debate.models import *
from django.contrib.auth.models import *
from pro_debate.sample_data import SampleData

class Command(BaseCommand):
    help = 'Give some basic data to work with'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # Create superuser
        aa = User.objects.create(
            username="aa", first_name="aa", is_superuser=True, is_staff=True)
        aa.set_password('aa')
        aa.save()

        sample_data = SampleData()
        sample_data.create_basics()

        
        print "You are the moon master!"