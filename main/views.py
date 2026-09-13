from django.shortcuts import render

from main.models import Experience, Education 


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
    context = {
        "name": "Mutia Muthmainnah",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)