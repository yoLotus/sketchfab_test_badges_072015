
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

# Create your tests here.
from django.contrib.auth.models import User
from badges_handler.models import Model3d, Creator3d, Badge
from badges_handler.crontab import PionnerBadgeCron

from freezegun import freeze_time
from datetime import datetime, timedelta

class BadgesTestCase(TestCase):

    def setUp(self):
        self.views_star_badges = settings.BADGES_SETTINGS['star']
        self.collector_threshold_badge = settings.BADGES_SETTINGS['collector']
        self.pionner = settings.BADGES_SETTINGS['pionner']

        user = User.objects.create_user('test', '', 'test')
        self.creator = Creator3d(user=user)
        self.creator.save()


    def tearDown(self):
        pass

    def test_view_is_updated(self):
        model_test = Model3d(name='test', description='test description',
                             creator=self.creator)
        number_of_views = model_test.number_of_views
        model_test.save()
        response = self.client.get(reverse('badges:detail_model',
                                           args=[model_test.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(number_of_views + 1,
                         Model3d.objects.get(pk=model_test.pk)
                         .number_of_views)

    def test_no_star_badge(self):
        model_test = Model3d(name='test', description='test description',
                             creator=self.creator)
        model_test.number_of_view = self.views_star_badges - 10
        model_test.save()
        self.assertEqual(model_test.badges.count(), 0)

        # add a new view
        self.client.get(reverse('badges:detail_model',
                                args=[model_test.pk]))
        self.assertEqual(model_test.badges.count(), 0)
        self.assertEqual(self.creator.badges.count(), 0)

    def test_star_badge_is_given(self):
        model_test = Model3d(name='test', description='test description',
                             creator=self.creator)
        model_test.number_of_views = self.views_star_badges - 1
        model_test.save()
        self.assertEqual(model_test.badges.count(), 0)
        self.assertEqual(self.creator.badges.count(), 0)

        # add a new view
        self.client.get(reverse('badges:detail_model',
                                args=[model_test.pk]))
        self.assertEqual(model_test.badges.count(), 1)
        self.assertEqual(self.creator.badges.count(), 1)

    def test_star_badge_dont_get_several_times(self):
        model_test = Model3d(name='test', description='test description',
                             creator=self.creator)
        model_test.number_of_views = self.views_star_badges - 1
        model_test.save()
        self.client.get(reverse('badges:detail_model',
                                args=[model_test.pk]))
        self.assertEqual(model_test.badges.count(), 1)
        self.assertEqual(self.creator.badges.count(), 1)
        self.client.get(reverse('badges:detail_model',
                                args=[model_test.pk]))
        # the model should not be starred a second time
        self.assertEqual(model_test.badges.count(), 1)
        self.assertEqual(self.creator.badges.count(), 1)

    def test_collector_badge(self):
        for i in range(self.collector_threshold_badge - 1):
            Model3d.objects.create(name='test', description='description',
                                   creator=self.creator)

        self.assertEqual(self.creator.badges.count(), 0)

        Model3d.objects.create(name='threshold', description='threshold',
                               creator=self.creator)
        self.assertEqual(self.creator.badges.count(), 1)

        Model3d.objects.create(name='threshold', description='threshold',
                               creator=self.creator)
        self.assertEqual(self.creator.badges.count(), 1)

    def test_pionner_badge(self):
        now_in_one_year = datetime.now() + timedelta(days=365)
        # in case the next year is leap
        if now_in_one_year.day != datetime.now().day:
            now_in_one_year = now_in_one_year + timedelta(days=1)

        cron_task = PionnerBadgeCron()
        with freeze_time(now_in_one_year):
            cron_task.do()
        self.assertEqual(self.creator.badges.count(), 1)
