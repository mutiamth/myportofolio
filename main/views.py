import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from main.models import Experience, Education, Project
from main.forms import EducationForm, ProjectForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan"
    )

    context = {
        "name": "Mutia Muthmainnah",
        "npm": "2506625230",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = { 
        "name": "Mutia Muthmainnah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    education = [item.object for item in education]

    context = {
        "name": "Mutia Muthmainnah",
        "education_list": education,
    }
    
    return render(request, "education.html", context)

def get_education_json(request):
    education = Education.objects.all()

    education_json = serializers.serialize(
        "json",
        education,
    )

    return HttpResponse(
        education_json,
        content_type="application/json"
    )

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education added successfully!")
            return redirect("main:show_education")

    context = {
        "name": "Mutia Muthmainnah",
        "form": form,
    }

    return render(request, "education_form.html", context)

def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)

        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully!")
            return redirect("main:show_education")
    else:
        form = EducationForm(instance=education)

    context = {
        "name": "Mutia Muthmainnah",
        "form": form,
    }

    return render(request, "education_form.html", context)

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education deleted successfully!")
        return redirect("main:show_education")

    return redirect("main:show_education")

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("main:show_projects")

    context = {
        "name": "Mutia Muthmainnah",
        "form": form,
    }

    return render(request, "project_form.html", context)

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": "Hanya pemilik portofolio yang dapat menambahkan proyek."
            },
            status=403,
        )

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save()

        return JsonResponse(
            {
                "message": "Proyek berhasil ditambahkan.",
                "pk": str(project.id),
            },
            status=201,
        )

    return JsonResponse(
        {
            "errors": form.errors.get_json_data()
        },
        status=400,
    )

@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (
        request.user.is_superuser
        or request.user.groups.filter(name="Editor").exists()
    ):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("main:show_projects")
    else:
        form = ProjectForm(instance=project)

    context = {
        "name": "Mutia Muthmainnah",
        "form": form,
        "is_edit": True,
    }

    return render(request, "project_form.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Mutia Muthmainnah",
        "title_query": title_query,
        "is_editor": is_editor,
        "form": ProjectForm(),
    }

    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []

    for project in projects:
        starred_users = project.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = Project.objects.get(pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

# =========================
# AUTHENTICATION
# =========================

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Mutia Muthmainnah",
        "form": form,
    }

    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Mutia Muthmainnah",
        "form": form,
    }

    return render(request, "login.html", context)

def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")

    return response