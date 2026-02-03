
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Project
from .models import Project, Task


@login_required
def dashboard(request):
    owned_projects = Project.objects.filter(owner=request.user)
    collaborated_projects = Project.objects.filter(
        collaborators=request.user
    ).exclude(owner=request.user)

    context = {
        'owned_projects': owned_projects,
        'collaborated_projects': collaborated_projects,
    }

    return render(request, 'tasks/dashboard.html', context)

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()

        # Solo owner o colaboradores pueden ver el proyecto
        if project.owner != request.user and request.user not in project.collaborators.all():
            raise PermissionDenied("No tienes acceso a este proyecto.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        total_tasks = project.total_tasks()
        done_tasks = project.completed_tasks()
        pending_tasks = total_tasks - done_tasks

        context['done_tasks'] = done_tasks
        context['pending_tasks'] = pending_tasks
        context['tasks'] = project.tasks.all()

        return context

from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'deadline', 'collaborators']
    template_name = 'tasks/project_form.html'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied("Solo el propietario puede editar el proyecto.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'tasks/project_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied("Solo el propietario puede borrar el proyecto.")
        return super().dispatch(request, *args, **kwargs)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        project = task.project

        if project.owner == request.user:
            self.fields = ['title', 'description', 'status', 'priority', 'assigned_to']
            return super().dispatch(request, *args, **kwargs)

        if request.user in project.collaborators.all():
            self.fields = ['status']
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("No tienes permiso para editar esta tarea.")

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})
