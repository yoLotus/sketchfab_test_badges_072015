"""Middleware to handler the Star badge

"""
from django.conf import settings
from django.db.models import F

from badges_handler.models import Model3d, Badge, Creator3d
from badges_handler.views import Model3dDetailView

STAR_BADGE_DETAIL_VIEW_FUNC = Model3dDetailView.as_view()


class StarBadgeMiddleWare:
    def process_view(self, request, view_func, *args, **kwargs):
        if view_func.__name__ == STAR_BADGE_DETAIL_VIEW_FUNC.__name__\
           and request.method.lower() == 'get':
            m = Model3d.objects.filter(pk=int(args[1]['pk']))
            if not m.first(): # do nothing particular, let Django raise 404 error
                return None
            m.update(number_of_views=F('number_of_views') + 1)

            # check the number of views for the star
            views_for_star_badges = settings.BADGES_SETTINGS.get('star', None)
            if views_for_star_badges\
               and m.first().number_of_views == views_for_star_badges:
                badge_star = Badge(content_object=m.first(),
                                   name='Star Model',
                                   description='This model has more than {} views'\
                                   .format(views_for_star_badges))
                badge_star.save()

        return None             # let other middlewares do their jobs
