from django.shortcuts import render

def home(request):
    return render(request, 'tree_menu/pages/home.html')

def about(request):
    return render(request, 'tree_menu/pages/about.html')

def services(request):
    return render(request, 'tree_menu/pages/services.html')

def contact(request):
    return render(request, 'tree_menu/pages/contact.html')