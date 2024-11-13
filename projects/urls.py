from django.urls import path
from .views import (
    project_list, create_project, update_project, delete_project,
    assign_volunteer, remove_volunteer, assigned_projects
)

urlpatterns = [
    path('projects/', project_list, name='project_list'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/update/<int:pk>/', update_project, name='update_project'),
    path('projects/delete/<int:pk>/', delete_project, name='delete_project'),
    path('projects/<int:project_id>/assign_volunteer/', assign_volunteer, name='assign_volunteer'),
    path('volunteer/remove/<int:participation_id>/', remove_volunteer, name='remove_volunteer'),
    path('assigned_projects/', assigned_projects, name='assigned_projects'),
]