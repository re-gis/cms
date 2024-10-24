from django.db import models
from accounts.models import CustomUser
from projects.models import Project

class VolunteerRecord(models.Model):
    """Model representing a volunteer's contribution to a project."""
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='volunteer_records')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='volunteer_records')
    hours_contributed = models.DecimalField(max_digits=5, decimal_places=2)
    contribution_date = models.DateField()

    def __str__(self):
        return f'{self.volunteer.username} - {self.project.title}'

    class Meta:
        db_table = "volunteer_records"