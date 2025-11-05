from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [

    path('', views.goals_index, name='home'),
    path('create/', views.goals_create, name='create'),
    #path("", views.goal_index, name="home"),                        
    #path("create/", views.goal_create, name="goal_create"),         
    #path("<int:goal_id>/", views.goal_detail, name="goal_detail"), 
    #path("<int:goal_id>/edit/", views.goal_edit, name="goal_edit"), 
    #path("<int:goal_id>/delete/", views.goal_delete, name="goal_delete"), 
]
