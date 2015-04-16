from django.core.management.base import BaseCommand, CommandError
from pro_debate.models import *
from django.contrib.auth.models import *

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

        Point.objects.bulk_create([
            Point(
                thesis="Life begins at conception.",
                thesis_elaborated="'Conception' is defined as the moment " + \
                "when a sperm and an egg fuse to become a zygote."),
            Point(thesis="Life begins at implantation."),
            Point(thesis="Life begins when the fetus can feel pain."),
            Point(thesis="Life begins when the fetus can retain memories."),
            Point(thesis="Life begins at birth."),
            Point(thesis="Life begins at conception."),
            Point(thesis="Life begins at 40."),
        ])

        self.prompt1 = Prompt.objects.create(prompt="When does life begin?")

        print "You are the moon master!"