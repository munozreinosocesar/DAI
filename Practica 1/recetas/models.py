# recetas/models.py
from django.db import models
from django.templatetags.static import static
from django.core.validators import FileExtensionValidator, RegexValidator

class Receta(models.Model):
    nombre       = models.CharField(max_length=200, validators=[RegexValidator(regex='^[A-Z].*$',message='Debe ser una cadena alfanumérica con la primera en mayuscula',code='invalid_username'),])
    preparación  = models.TextField(max_length=5000)
    foto         = models.FileField(null=True, blank=True, validators=[FileExtensionValidator(['png'])])

    def __str__(self):
        return self.nombre

    def foto_url(self):
      return static("media/{}".format(self.foto))

class Ingrediente(models.Model):
    nombre        = models.CharField(max_length=200, validators=[RegexValidator(regex='^[A-Z].*$',message='Debe ser una cadena alfanumérica con la primera en mayuscula',code='invalid_username'),])
    cantidad      = models.PositiveSmallIntegerField()
    unidades      = models.CharField(max_length=5)
    receta        = models.ForeignKey(Receta, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
