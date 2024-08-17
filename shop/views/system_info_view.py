from django.http import HttpResponse
from django.shortcuts import render

def system_info(request):
    context = {
        'project_name': 'Cash Register',
        'version': '1.0',
        'author': 'anxnas',
        'description': 'This is a simple cash register system built with Django.',
    }
    return render(request, 'system_info.html', context)