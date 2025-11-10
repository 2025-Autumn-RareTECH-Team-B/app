from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [

    path('', views.goals_index, name='home'),
    path('create/', views.goals_create, name='create'),                             
    path("<int:goal_id>/", views.goals_detail, name="goal_detail"), 
    path("<int:goal_id>/edit/", views.goals_edit, name="goal_edit"), 
    path("<int:goal_id>/delete/", views.goals_delete, name="goal_delete"), 
]
