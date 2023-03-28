# recetas/views.py

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Ingrediente, Receta
from django.db.models import Q
from .forms import RecetasForm, IngredientesForm, UserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, 'home.html', {})


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserCreationForm
    success_message = "Usuario creado correctamente"

class SignUpUsersView(SuccessMessageMixin, CreateView):
    template_name = 'registration/signup_user.html'
    success_url = reverse_lazy('login')
    form_class = UserForm
    success_message = "Usuario creado correctamente"



class RecetasList(ListView):
    model = Receta
    template_name = 'recetas/recetas_list.html'


class SearchResultsView(ListView):
    model = Receta
    template_name = 'recetas/recetas_search.html'

    def get_queryset(self):
        query = self.request.GET.get('receta_search')
        object_list = Receta.objects.filter(Q(nombre__icontains=query))
        return object_list


class RecetasDetail(DetailView):
    model = Receta
    template_name = 'recetas/recetas_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecetasDetail, self).get_context_data(**kwargs)
        return context


class RecetasDelete(DeleteView):
    model = Receta
    success_url = reverse_lazy('recetas_list')
    success_message = "Eliminado correctamente"
    def delete(self, request, *args, **kwargs):
            messages.success(self.request, self.success_message)
            return super(RecetasDelete, self).delete(request, *args, **kwargs)

class RecetasUpdate(SuccessMessageMixin, UpdateView):
    model = Receta
    form_class = RecetasForm
    template_name = 'recetas/recetas_update.html'
    success_url = reverse_lazy('recetas_list')
    success_message = "Actualizado correctamente"


class RecetasNew(SuccessMessageMixin, CreateView):
    model = Receta
    form_class = RecetasForm
    template_name = 'recetas/recetas_update.html'
    success_url = reverse_lazy('recetas_list')
    success_message = "Creado correctamente"



class IngredientesList(ListView):
    model = Ingrediente
    template_name = 'ingredientes/ingredientes_list.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientesList, self).get_context_data(**kwargs)
        context['ingredientes'] = Ingrediente._meta.get_fields()
        return context

class IngredientesDetail(DetailView):
    model = Ingrediente
    template_name = 'ingredientes/ingredientes_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IngredientesDetail, self).get_context_data(**kwargs)
        return context


class IngredientesDelete(DeleteView):
    model = Ingrediente
    success_url = reverse_lazy('ingredientes_list')
    success_message = "Eliminado correctamente"
    def delete(self, request, *args, **kwargs):
            messages.success(self.request, self.success_message)
            return super(IngredientesDelete, self).delete(request, *args, **kwargs)

class IngredientesUpdate(SuccessMessageMixin, UpdateView):
    model = Ingrediente
    form_class = IngredientesForm
    template_name = 'ingredientes/ingredientes_update.html'
    success_url = reverse_lazy('ingredientes_list')
    success_message = "Actualizado correctamente"


class IngredientesNew(SuccessMessageMixin, CreateView):
    model = Ingrediente
    form_class = IngredientesForm
    template_name = 'ingredientes/ingredientes_update.html'
    success_url = reverse_lazy('ingredientes_list')
    success_message = "Creado correctamente"



def dark_light_theme(request):
    theme = request.session.get('theme')

    if theme == 'dark':
        request.session['theme'] = 'light'
    else:
        request.session['theme'] = 'dark'

    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', '/'))
