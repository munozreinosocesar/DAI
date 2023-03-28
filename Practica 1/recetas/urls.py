# recetas/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RecetasList.as_view(), name='home'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('signup_users', views.SignUpUsersView.as_view(), name='signup_users'),

    path('recetas_list', views.RecetasList.as_view(), name='recetas_list'),
    path('recetas_search', views.SearchResultsView.as_view(), name='recetas_search'),
    path('recetas_detail/<int:pk>', views.RecetasDetail.as_view(), name='recetas_detail'),
    path('recetas_delete/<int:pk>', views.RecetasDelete.as_view(), name='recetas_delete'),
    path('recetas_update/<int:pk>', views.RecetasUpdate.as_view(), name='recetas_update'),
    path('recetas_new', views.RecetasNew.as_view(), name='recetas_new'),

    path('ingredientes_list', views.IngredientesList.as_view(), name='ingredientes_list'),
    path('ingredientes_detail/<int:pk>', views.IngredientesDetail.as_view(), name='ingredientes_detail'),
    path('ingredientes_delete/<int:pk>', views.IngredientesDelete.as_view(), name='ingredientes_delete'),
    path('ingredientes_update/<int:pk>', views.IngredientesUpdate.as_view(), name='ingredientes_update'),
    path('ingredientes_new', views.IngredientesNew.as_view(), name='ingredientes_new'),

	path('dark_light_theme/', views.dark_light_theme, name="dark_light_theme"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
