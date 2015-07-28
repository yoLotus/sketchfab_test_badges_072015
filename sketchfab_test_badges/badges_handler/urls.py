from django.conf.urls import include, url

from badges_handler.views import Model3dDetailView, Model3dCreateView,\
    check_new_user, Creator3dDetailView, Creator3dTemplateView

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # namespace = badges
    url(r'^models/(?P<pk>[0-9]+)$', Model3dDetailView.as_view(), name="detail_model"),
    url(r'^users/(?P<pk>[0-9]+)$', Creator3dDetailView.as_view(), name="users_model"),
    url(r'^models/create$', login_required(Model3dCreateView.as_view()), name="model_create"),
    url(r'^users/create$', Creator3dTemplateView.as_view(), name="user_create"),
    url(r'^users/check$', check_new_user, name='check'),
    url(r'^login', auth_views.login, {'template_name': 'badges_handler/login.html'},
        name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
]
