from django.shortcuts import render
from django.views import generic

from badges_handler.models import Model3d, Creator3d

# Create your views here.

class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creators'] = Creator3d.objects.all()
        context['models'] = Model3d.objects.all()
        return context


class Model3dDetailView(generic.DetailView):
    model = Model3d
    context_object_name = "model3d"


class Creator3dDetailView(generic.DetailView):
    model = Creator3d
    context_object_name = "creator"
