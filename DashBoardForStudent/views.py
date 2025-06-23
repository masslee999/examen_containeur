from django.shortcuts import render

from StudentList.models import DevStudents


def home(request):
    """returns the list of the students registered"""
    students = DevStudents.objects.all()
    return render(request,'index.html', context={'students':students})

# def get_students_json(request):
#     students = DevStudents.objects.all()
#
#     return JSONResponse()