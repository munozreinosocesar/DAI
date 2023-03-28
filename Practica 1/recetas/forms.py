from django import forms
from .models import Receta, Ingrediente
from django.contrib.auth.forms import UserCreationForm, User

class RecetasForm(forms.ModelForm):


    class Meta:
        model = Receta
        fields = ('nombre', 'preparación', 'foto')

        widgets = {
			'nombre': forms.TextInput,
			'preparación': forms.Textarea(attrs={'rows':5})
		}

class IngredientesForm(forms.ModelForm):


    class Meta:
        model = Ingrediente
        fields = ('nombre', 'cantidad', 'unidades', 'receta')

        widgets = {
			'nombre': forms.TextInput,
		}

class UserForm(UserCreationForm):


    class Meta:
        model = User
        fields = ('username' ,'password1' ,'is_staff',)

        widgets = {
			'username': forms.TextInput,
		}

