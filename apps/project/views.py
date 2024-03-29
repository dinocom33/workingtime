from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from copy import deepcopy

from .models import Project, Task, Entry
from apps.team.models import Team
from apps.main.decorators import allowed_users, admin_only


@login_required(login_url='login')
def projects(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.filter(status=Project.ACTIVE)
    archived_projects = team.projects.filter(status=Project.ARCHIVED)

    if request.method == "POST":
        title = request.POST.get('title')

        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)

            messages.info(request, "Project was created successfully")

            return redirect('project:projects')

    return render(request, 'project/projects.html', {"team": team, "projects": projects, 'archived_projects': archived_projects})


@login_required(login_url='login')
def project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            task = Task.objects.create(team=team, project=project, created_by=request.user, title=title)

            messages.info(request, 'Task was created successfully')

            return redirect("project:project", project_id=project.id)

    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)
    tasks_archived = project.tasks.filter(status=Task.ARCHIVED)

    return render(request, "project/project.html",
                  {"team": team, "project": project, "tasks_todo": tasks_todo, "tasks_done": tasks_done,
                   'tasks_archived': tasks_archived})


@login_required(login_url='login')
@admin_only
def edit_project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == "POST":
        title = request.POST.get('title')
        status = request.POST.get('status')

        if title:
            project.title = title
            project.status = status
            project.save()

            messages.info(request, "Changes was saved successfully")

            return redirect("project:project", project_id=project.id)

    return render(request, "project/edit_project.html", {"team": team, "project": project})


@login_required(login_url='login')
def task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == "POST":
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        total_minutes = (hours * 60) + minutes

        entry = Entry.objects.create(team=team, project=project, task=task, minutes=total_minutes,
                                     created_by=request.user, created_at=date, is_tracked=True)

    return render(request, "project/task.html",
                  {"today": datetime.today(), "team": team, "project": project, "task": task})


@login_required(login_url='login')
@admin_only
def edit_task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == "POST":
        title = request.POST.get('title')
        status = request.POST.get('status')

        if title:
            task.title = title
            task.status = status
            task.save()

            messages.info(request, "Task was saved successfully")

            return redirect('project:task', project_id=project_id, task_id=task_id)

    return render(request, "project/edit_task.html", {"team": team, "project": project, "task": task})


@login_required(login_url='login')
def edit_entry(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)

    if request.method == "POST":
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()
        messages.info(request, "Changes was saved successfully")

        return redirect('project:task', project_id=project_id, task_id=task_id)

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        "team": team,
        "project": project,
        "task": task,
        "entry": entry,
        "hours": hours,
        "minutes": minutes,
    }

    return render(request, 'project/edit_entry.html', context)


@login_required(login_url='login')
def delete_entry(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, "The entry has been deleted successfully")

    return redirect("project:task", project_id=project_id, task_id=task_id)


@login_required(login_url='login')
def delete_untracked_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, "The entry has been deleted successfully")

    return redirect("dashboard")


@login_required(login_url='login')
def track_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    projects = team.projects.filter(status=Project.ACTIVE)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = request.POST.get('project')
        task = request.POST.get('task')

        if project and task:
            entry.project_id = project
            entry.task_id = task
            entry.minutes = (hours * 60) + minutes
            entry.created_at = '%s %s' % (request.POST.get('date'), entry.created_at.time())
            entry.is_tracked = True
            entry.save()

            messages.info(request, 'Your time has been tracked')

            return redirect('dashboard')

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'hours': hours,
        'minutes': minutes,
        'team': team,
        'projects': projects,
        'entry': entry,
    }

    return render(request, 'project/track_entry.html', context)


@login_required(login_url='login')
@admin_only
def clone_project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = Project.objects.filter(team=team, pk=project_id).get()
    tasks = Task.objects.filter(project=project)
    new_project = deepcopy(project)

    if request.method == "POST":
        new_project.title = request.POST.get('title')
        new_project.team = project.team
        new_project.created_by = request.user
        new_project.create_at = datetime.now()
        new_project.pk = None

        new_project.save()

        for task in tasks:
            new_task = deepcopy(task)
            new_task.pk = None
            new_task.project = new_project
            new_task.save()

        messages.info(request, "Project was cloned successfully")

        return redirect("project:project", project_id=new_project.id)

    return render(request, "project/edit_project.html", {"team": team, "project": project})
