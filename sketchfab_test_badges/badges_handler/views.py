from django.shortcuts import render
from django.views import generic

from badges_handler.models import Model3d

# Create your views here.


class Model3dDetailView(generic.DetailView):
    model = Model3d
    context_object_name = "model3d"
