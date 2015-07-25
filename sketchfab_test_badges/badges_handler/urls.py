from django.conf.urls import include, url

from badges_handler.views import Model3dDetailView

# namespace = models
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', Model3dDetailView.as_view(), name="detail_model")
]
