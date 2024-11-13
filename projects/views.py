from django.shortcuts import render, redirect, get_object_or_404
from notifications.utils import send_email_notification
from .models import Project, VolunteerParticipation
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProjectForm
from accounts.models import CustomUser
from volunteers.models import VolunteerRecord
from django.db.models import Count
from django.http import JsonResponse, HttpResponse


def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def project_list(request):
    projects = Project.objects.all()
    ps = Project.objects.annotate(volunteer_count=Count('participations'))

    project_number = projects.count()
    user = request.user
    volunteers = CustomUser.objects.filter(role='volunteer').count() - 1
    
    ongoing_projects = projects.filter(status='ongoing').count()
    planned_projects = projects.filter(status='planned').count()
    completed_projects = projects.filter(status='completed').count()
    
    unassigned_projects_count = ps.filter(volunteer_count=0).count()


    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'ongoing_projects': ongoing_projects,
        'planned_projects': planned_projects,
        'completed_projects': completed_projects,
        "user": user,
        "volunteers": volunteers,
        "project_number": project_number,
        'unassigned_projects_count': unassigned_projects_count 
    })

@login_required
@user_passes_test(is_staff)
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            messages.success(request, 'Project created successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        
        if form.is_valid():
            print(form.cleaned_data)  # Debug: Check if the 'status' is in cleaned_data
            updated_project = form.save(commit=False)
            updated_project.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_list')
        else:
            print(form.errors)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/update_project.html', {'form': form, 'project': project})

@login_required
@user_passes_test(is_staff)
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('project_list')
    return render(request, 'projects/delete_project.html', {'project': project})

@login_required
@user_passes_test(is_staff)
def assign_volunteer(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        volunteer_id = request.POST.get('volunteer')
        volunteer = get_object_or_404(CustomUser, pk=volunteer_id)

        if VolunteerParticipation.objects.filter(volunteer=volunteer, project=project).exists():
            messages.warning(request, f"{volunteer.username} is already assigned to {project.title}.")
            return redirect('project_list')

        VolunteerParticipation.objects.get_or_create(volunteer=volunteer, project=project)

        # Send email notification
        subject = f'You Have Been Assigned to {project.title}'
        message = f'Hello {volunteer.username},\n\nYou have been assigned to the project "{project.title}". Thank you for your participation!\n\nBest regards,\nD Regis'
        send_email_notification(volunteer.email, subject, message)

        messages.success(request, f"{volunteer.username} has been assigned to {project.title} and email sent.")
        return redirect('project_list')

    volunteers = CustomUser.objects.filter(is_active=True, role='volunteer')
    return render(request, 'projects/assign_volunteer.html', {'project': project, 'volunteers': volunteers})

@login_required
@user_passes_test(is_staff)
def remove_volunteer(request, participation_id):
    participation = get_object_or_404(VolunteerParticipation, pk=participation_id)
    if request.method == 'POST':
        participation.delete()
        subject = f'You Have Been removed from {participation.project.title}'
        message = f'Hello {participation.volunteer.username},\n\nYou have been assigned to the project "{participation.project.title}". Thank you for your participation!\n\nBest regards,\nD Regis'
        send_email_notification(participation.volunteer.email, subject, message)
        messages.success(request, 'Volunteer removed from project.')
        return redirect('project_list')
    return render(request, 'projects/remove_volunteer.html', {'participation': participation})


def assigned_projects(request):
    projects = Project.objects.filter(volunteers=request.user) 

    ongoing_count = projects.filter(status='ongoing').count()
    planned_count = projects.filter(status='planned').count()
    completed_count = projects.filter(status='completed').count()

    
    context = {
        'projects': projects,
        'project_number': projects.count(),
        'ongoing_projects': ongoing_count,
        'planned_projects': planned_count,
        'completed_projects': completed_count,
    }

    return render(request, 'projects/assigned_projects.html', context)
