from django.shortcuts import render, redirect, get_object_or_404
from notifications.utils import send_email_notification
from .models import Project, VolunteerParticipation
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProjectForm
from accounts.models import CustomUser

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

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
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_list')
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
        VolunteerParticipation.objects.get_or_create(volunteer=volunteer, project=project)
        #  send notif
        subject = f'You Have Been Assigned to {project.title}'
        message = f'Hello {volunteer.username},\n\nYou have been assigned to the project "{project.title}". Thank you for your participation!\n\nBest regards,\nD Regis'
        send_email_notification(volunteer.email, subject, message)
        messages.success(request, f"{volunteer.username} has been assigned to {project.title}.")
        return redirect('project_list')
    volunteers = CustomUser.objects.filter(is_active=True)
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


@login_required
def assigned_projects(request):
    if request.user.is_volunteer():
        volunteer_projects = Project.objects.filter(volunteers=request.user)
        return render(request, 'projects/assigned_projects.html', {'projects': volunteer_projects})
    else:
        return render(request, 'projects/assigned_projects.html', {'projects': []})