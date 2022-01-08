from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'website/index.html')

def productos(request):
    return render(request, 'website/mostrar-productos.html')


def dashboard(request):
    return render(request, 'dashboard/index.html')