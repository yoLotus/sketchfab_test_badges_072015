"""define tasks to run periodically for badges app

"""

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
        print('pionner !')
        creators = Creator3d.objects.filter(date_creation_sign_in__day=now.day,
                                            date_creation_sign_in__month=now.month,
                                            date_creation_sign_in__year=now.year - 1)

        for c in creators:
            Badge.objects.create(content_object=c,
                                 name='Pionner',
                                 description='It has been more than 1 year you sign in')
