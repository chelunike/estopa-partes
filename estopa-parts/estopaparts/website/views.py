import re
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict

from .models import *
from .forms import RegisterForm

def check_login(level):
    print('Check login access: ', level)
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if 'user' not in request.session:
                return redirect('login')

            return func(request, *args, **kwargs)

        return wrapper
    return inner

# Create your views here.
def index(request):
    if 'noty' not in request.session:
       request.session['noty'] = []
    data = {
        'noty': request.session['noty']
    }

    return render(request, 'website/index.html', data)

def login(request):
    if 'noty' not in request.session:
       request.session['noty'] = []

    data = {
        'title': 'Login',
        'noty': request.session['noty']
    }

    if request.method == 'POST' and 'email' in request.POST and 'clave' in request.POST:
        try:
            usuario = Usuario.objects.get(correo=request.POST['email'])
            
            if check_password(request.POST['clave'], usuario.clave):
                request.session['user'] = model_to_dict(usuario)
                request.session['noty'] = [{'type': 'success', 'msg': 'Login completado con exito.'}]
                return redirect('dashboard')
        except Exception as e:
            print('Login error: ', e)
        request.session['noty'] = [{'type': 'alert', 'msg': 'Error al acceder.'}]

    return render(request, 'website/login.html', data)

def logout(request):
    del request.session['user']
    return redirect('login')


def register(request):
    form = RegisterForm(request.POST or None)
    data = {
        'title': 'Registro',
        'form': form,
        'noty': request.session['noty']
    }

    if request.method == 'POST':
        if form.is_valid():
            
            # Create password hash
            form.cleaned_data['clave'] = make_password(form.cleaned_data['clave'])
            clean_data = form.cleaned_data
            record = Usuario.objects.create(**clean_data)

            request.session['noty'] = [{'type': 'success', 'msg': 'Registro completado con exito.'}]
            return redirect('login')
        else:
            request.session['noty'] = [{'type': 'alert', 'msg': 'Error en los datos al registrarse.'}]
            return render('register')
    
    return render(request, 'website/register.html', data)





def productos(request):
    if 'noty' not in request.session:
       request.session['noty'] = []
    if 'carrito' not in request.session:
       request.session['carrito'] = []
    
    if request.method == 'POST':
        value=request.POST['submit']
        if value=='añadir':
            producto =  model_to_dict(Producto.objects.get(pk=request.POST['id']))
            producto['imagen'] = str(producto['imagen'])
            request.session['carrito'].append(producto)
            request.session.modified = True
        if value=='borrar':
            producto =  model_to_dict(Producto.objects.get(pk=request.POST['id']))
            producto['imagen'] = str(producto['imagen'])
            for p in request.session['carrito']:
                if p['id'] == producto['id']:
                    request.session['carrito'].remove(p)
                    request.session.modified = True
    id=[]
    for p in request.session['carrito']:
        id.append(p['id'])
    data = {
        'productos': Producto.objects.all(),
        "carrito": request.session['carrito'],
        "id": id
    }
    return render(request, 'website/mostrar-productos.html', data)

def carrito(request):
    #if 'noty' not in request.session:
    #   request.session['noty'] = []
    
    data={
        "carrito": request.session['carrito']
    }
    
    
    return render(request, 'website/carrito.html', data)

@check_login(1)
def dashboard(request):
    data = {
        'title': 'Panel de control',
    }
    return render(request, 'dashboard/index.html', data)