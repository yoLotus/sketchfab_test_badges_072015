from django.conf.urls import include, url

from badges_handler.views import Model3dDetailView, Creator3dDetailView

urlpatterns = [
    # namespace = badges
    url(r'^models/(?P<pk>[0-9]+)$', Model3dDetailView.as_view(), name="detail_model"),
    url(r'^users/(?P<pk>[0-9]+)$', Creator3dDetailView.as_view(), name="users_model")
]
