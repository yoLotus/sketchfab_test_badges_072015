"""define tasks to run periodically for badges app

"""
import itertools

from django_cron import CronJobBase, Schedule
from django.conf import settings
from badges_handler.models import Creator3d, Badge, Model3d

from datetime import datetime


class PionnerBadgeCron(CronJobBase):
    RUN_AT_TIMES = settings.BADGES_SETTINGS.get('pionner', [])
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'badges_handler.pionner_badge'

    def do(self):
        now = datetime.now()
        creators = Creator3d.objects.filter(date_creation_sign_in__day=now.day,
                                            date_creation_sign_in__month=now.month,
                                            date_creation_sign_in__year=now.year - 1)

        # in case of leap year
        creators_leap = []
        if now.day == 29 and now.month == 2:
            creators_leap = Creator3d.objects.filter(date_creation_sign_in__day=1,
                                                     date_creation_sign_in__month=3,
                                                     date_creation_sign_in__year=now.year - 1)

        for c in itertools.chain(creators, creators_leap):
            Badge.objects.create(content_object=c,
                                 name='Pionner',
                                 description='It has been more than 1 year you sign in',
                                 creator3d=c)
