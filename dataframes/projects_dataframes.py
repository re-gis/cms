import os
import sys
import django  # type: ignore
import pandas as pd  # type: ignore
from django.db import models

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from projects.models import Project, VolunteerParticipation

projects = Project.objects.all().values(
    'id', 'title', 'description', 'creator__username', 'start_date', 'end_date', 'status'
)
projects_df = pd.DataFrame(list(projects))
print("Projects DataFrame:")
print(projects_df)



participations = VolunteerParticipation.objects.all().values(
    'id', 'volunteer__username', 'project__title', 'hours_contributed'
)

participations_df = pd.DataFrame(list(participations))
print("\nVolunteer Participations DataFrame:")
print(participations_df)



projects_with_volunteers = Project.objects.all().annotate(
    volunteer_count=models.Count('volunteers')
).values('id', 'title', 'description', 'volunteer_count')
projects_with_volunteers_df = pd.DataFrame(list(projects_with_volunteers))
print("\nProjects with Volunteer Count DataFrame:")
print(projects_with_volunteers_df)





volunteer_hours = VolunteerParticipation.objects.values(
    'volunteer__username'
).annotate(total_hours=models.Sum('hours_contributed'))
volunteer_hours_df = pd.DataFrame(list(volunteer_hours))
print("\nVolunteers and Their Total Hours Contributed DataFrame:")
print(volunteer_hours_df)




project_hours = VolunteerParticipation.objects.values(
    'project__title'
).annotate(total_hours=models.Sum('hours_contributed'))
project_hours_df = pd.DataFrame(list(project_hours))
print("\nProjects and Their Total Volunteer Hours DataFrame:")
print(project_hours_df)



active_projects = projects_df[projects_df['status'] == 'ongoing']
print("\nActive/Ongoing Projects DataFrame:")
print(active_projects)



completed_projects = projects_df[projects_df['status'] == 'completed']
print("\nCompleted Projects DataFrame:")
print(completed_projects)


planned_projects = projects_df[projects_df["status"] == 'planned']
print("\Planned Projects DataFrame:")
print(planned_projects)





volunteer_projects = VolunteerParticipation.objects.all().values(
    'volunteer__username', 'project__title'
)
volunteer_projects_df = pd.DataFrame(list(volunteer_projects))
print("\nVolunteers with Projects They Participated In DataFrame:")
print(volunteer_projects_df)


projects_df.to_csv('projects.csv', index=False)
print("\nExported 'projects.csv' successfully!")

participations_df.to_csv('participations.csv', index=False)
print("Exported 'participations.csv' successfully!")

projects_with_volunteers_df.to_csv('projects_with_volunteers.csv', index=False)
print("Exported 'projects_with_volunteers.csv' successfully!")

volunteer_hours_df.to_csv('volunteer_hours.csv', index=False)
print("Exported 'volunteer_hours.csv' successfully!")

project_hours_df.to_csv('project_hours.csv', index=False)
print("Exported 'project_hours.csv' successfully!")

active_projects.to_csv('active_projects.csv', index=False)
print("Exported 'active_projects.csv' successfully!")

completed_projects.to_csv('completed_projects.csv', index=False)
print("Exported 'completed_projects.csv' successfully!")

planned_projects.to_csv('planned_projects.csv', index=False)
print("Exported 'planned_projects.csv' successfully!")

volunteer_projects_df.to_csv('volunteer_projects.csv', index=False)
print("Exported 'volunteer_projects.csv' successfully!")