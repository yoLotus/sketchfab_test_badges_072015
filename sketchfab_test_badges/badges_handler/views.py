import itertools
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic

from badges_handler.models import Model3d, Creator3d

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.


class IndexTemplateView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creators'] = Creator3d.objects.all()
        # context['models'] = Model3d.objects.all()
        models = Model3d.objects.all()
        if self.request.user.is_authenticated():
            creator = Creator3d.objects.get(user=self.request.user)
            context['models_current_creators'] = models.filter(creator=creator)
            context['others_models'] = models.exclude(creator=creator)
        else:
            context['models'] = models
        return context


class Model3dCreateView(generic.CreateView):
    model = Model3d
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.creator = Creator3d.objects.get(user=self.request.user)
        form.instance.number_of_view = 0
        return super().form_valid(form)



class Model3dDetailView(generic.DetailView):
    model = Model3d
    context_object_name = "model3d"


class Creator3dDetailView(generic.DetailView):
    model = Creator3d
    context_object_name = "creator"


class Creator3dTemplateView(generic.TemplateView):
    template_name = 'badges_handler/sign_in.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreationForm()
        return context


class NewCreator3dTemplateView(generic.TemplateView):
    template_name = 'badges_handler/sign_in.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreationForm()
        return context


def check_new_user(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            data = user_form.cleaned_data
            user = User.objects.create_user(data['username'], '', data['password1'])
            Creator3d.objects.create(user=user)
            return HttpResponseRedirect(request.POST['next'])
        else:
            return HttpResponseRedirect(reverse('badges:create'))
    else:
        return HttpResponse(reverse('index'))
