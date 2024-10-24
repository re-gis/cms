from django.db import models
from accounts.models import CustomUser

class Project(models.Model):
    """Model representing a community project."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects')
    volunteers = models.ManyToManyField(CustomUser, through='VolunteerParticipation', related_name='volunteered_projects', blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], default='planned')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "projects"

class VolunteerParticipation(models.Model):
    """Model for tracking volunteer participation in projects."""
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='participations', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='participations')
    hours_contributed = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.volunteer.username} in {self.project.title}'

    class Meta:
        db_table = "volunteer_participation"
