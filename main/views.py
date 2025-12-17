from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    """
    Home page view - displays the main landing page
    """
    context = {
        'title': 'Welcome to Django Web',
        'message': 'This is a Django application with frontend and backend integration.',
    }
    return render(request, 'main/home.html', context)

def about(request):
    """
    About page view - displays information about the project
    """
    context = {
        'title': 'About Us',
        'description': 'This is a Django web application demonstrating frontend and backend display screens.',
        'features': [
            'Django Backend',
            'HTML Templates',
            'Static Files (CSS/JS)',
            'URL Routing',
            'Template Context',
        ]
    }
    return render(request, 'main/about.html', context)

def contact(request):
    """
    Contact page view - displays contact information
    """
    context = {
        'title': 'Contact Us',
        'email': 'info@djangoweb.com',
        'phone': '+123 456 7890',
    }
    return render(request, 'main/contact.html', context)
