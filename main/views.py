from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Experience, Education, Project
from main.forms import EducationForm, ProjectForm
from django.core import serializers
from django.http import HttpResponse

def show_main(request):
    context = {
        "name": "Mutia Muthmainnah",
        "npm": "2506625230",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
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

def create_project(request):
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

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Mutia Muthmainnah",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)

    return HttpResponse(
        projects_json,
        content_type="application/json"
    )

def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")