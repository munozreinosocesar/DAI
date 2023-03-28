from django.contrib import admin, messages
from .models import Ingrediente, Receta

# Register your models here.

admin.site.site_header = 'Mis recetas'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Recetas'

class IngredienteAdmin(admin.ModelAdmin):
      list_display = ('nombre', 'cantidad', 'unidades', 'receta')
      search_fields = ('nombre', 'cantidad', 'unidades', 'receta')
      fields = ('nombre', 'cantidad', 'unidades', 'receta')
      ordering = ('-nombre',)

      def sin_stock(modeladmin, request, queryset):
        queryset.update(cantidad=0.0)
        messages.success(request, "Se eliminó el stock")
      admin.site.add_action(sin_stock, "Eliminar stock")

class RecetaAdmin(admin.ModelAdmin):
      list_display = ('nombre', 'preparación', 'foto','tiene_foto')
      search_fields = ('nombre', 'preparación', 'foto')
      fields = ('nombre', 'preparación', 'foto')
      ordering = ('-nombre',)

      def tiene_foto(self, obj):
        return "Tiene foto" if obj.foto is not None else "No tiene de foto"



admin.site.register(Ingrediente, IngredienteAdmin)

admin.site.register(Receta, RecetaAdmin)
