from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    collaborators = models.ManyToManyField(
        User,
        related_name='collaborated_projects',
        blank=True
    )

    def clean(self):
        if self.deadline < timezone.now().date():
            raise ValidationError("La fecha límite no puede estar en el pasado.")

    def total_tasks(self):
        return self.tasks.count()

    def completed_tasks(self):
        return self.tasks.filter(status='DONE').count()

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'Pendiente'),
        ('INPROG', 'En Progreso'),
        ('DONE', 'Completada'),
    ]
    PRIORITY_CHOICES = [
        ('L', 'Baja'),
        ('M', 'Media'),
        ('H', 'Alta'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

