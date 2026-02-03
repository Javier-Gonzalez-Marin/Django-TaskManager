from django.urls import path
from . import views
from .views import ProjectDetailView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]

from django.urls import path
from . import views
from .views import (
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskUpdateView,
)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
]
