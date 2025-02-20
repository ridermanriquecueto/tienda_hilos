# Hilos/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Asegúrate de crear una plantilla home.html
