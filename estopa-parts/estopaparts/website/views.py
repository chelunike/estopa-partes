import re
from tkinter.tix import Form
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict

from .models import *
from .forms import RegisterForm, ProfileForm, PasswordForm, ProductForm

def check_login(level):
    #print('Check login access: ', level)
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if 'user' not in request.session:
                return redirect('login')
            elif request.session['user']['tipo'] > level:
                return redirect('login')

            return func(request, *args, **kwargs)
        return wrapper
    return inner

def session(func):
    def wrapper(request, *args, **kwargs):
        if 'noty' not in request.session:
            request.session['noty'] = []
        
        result = func(request, *args, **kwargs)
        # Clean norifications
        request.session['noty'] = []
        return result
    return wrapper


# Create your views here.
@session
def index(request):
    data = {
        'noty': request.session['noty']
    }

    return render(request, 'website/index.html', data)

@session
def login(request):
    if request.method == 'POST' and 'email' in request.POST and 'clave' in request.POST:
        try:
            usuario = Usuario.objects.get(correo=request.POST['email'])
            
            if check_password(request.POST['clave'], usuario.clave):
                request.session['user'] = model_to_dict(usuario)
                request.session['noty'] = [{'type': 'success', 'msg': 'Login completado con exito.'}]
                return redirect('dashboard')
        except Exception as e:
            print('Login error: ', e)
        request.session['noty'] = [{'type': 'error', 'msg': 'Error al acceder.'}]
    data = {
        'title': 'Login',
        'noty': request.session['noty']
    }
    return render(request, 'website/login.html', data)

@session
def logout(request):
    del request.session['user']
    return redirect('login')


@session
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
            if record.tipo == 1:
                Vendedor.objects.create(id_usuario=record.id)
            elif record.tipo == 2:
                Comprador.objects.create(id_usuario=record.id)
            request.session['noty'] = [{'type': 'success', 'msg': 'Registro completado con exito.'}]
            return redirect('login')
        else:
            request.session['noty'] = [{'type': 'error', 'msg': 'Error en los datos al registrarse.'}]
            return render('register')
    
    return render(request, 'website/register.html', data)

@session
def productos(request):
    if 'noty' not in request.session:
       request.session['noty'] = []
    if 'carrito' not in request.session:
       request.session['carrito'] = []
    id=[]
    data = {
        'productos': Producto.objects.all(),
        "carrito": request.session['carrito'],
        "web": "productos",
        "id": id
    }
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
            if request.POST['web']=="carrito":
                data["web"]="carrito"
                return render(request, 'website/carrito.html', data)
        
    
    for p in request.session['carrito']:
        id.append(p['id'])
    
    
    return render(request, 'website/mostrar-productos.html', data)

@session
def carrito(request):
    final = 0
    total = 0
    descuento = 0
    for p in request.session['carrito']:
        producto =  Producto.objects.get(pk=p['id'])
        total += producto.precio
        final += producto.getPrecio()

    descuento = final - total
    data = {
        "carrito": request.session['carrito'],
        "web": "carrito",
        "final":final,
        "total":total,
        "descuento":descuento
    }

    return render(request, 'website/carrito.html', data)

@check_login(1)
@session
def dashboard(request):
    data = {
        'title': 'Panel de control',
        'noty': request.session['noty'],
        'user': request.session['user']
    }
    return render(request, 'dashboard/index.html', data)

@check_login(2)
@session
def profile(request):
    profile_form = ProfileForm(request.POST or None, instance=Usuario.objects.get(pk=request.session['user']['id']))
    passwd_form = PasswordForm(request.POST or None)

    if request.method == 'POST':
        if profile_form.is_valid(): # -- -- Datos del Usuario -- --
            profile_form.save()
            request.session['noty'] = [{'type': 'success', 'msg': 'Datos actualizados con exito.'}]
            request.session['user'].update(profile_form.cleaned_data)
            request.session.modified = True
        if passwd_form.is_valid(): # -- -- Contraseña -- --
            usuario = Usuario.objects.get(pk=request.session['user']['id'])
            if check_password(passwd_form.cleaned_data['claveAntigua'], usuario.clave):
                usuario.clave = make_password(passwd_form.cleaned_data['clave'])
                usuario.save()
                request.session['noty'] = [{'type': 'success', 'msg': 'Clave actualizada con exito.'}]
            else:
                request.session['noty'] = [{'type': 'error', 'msg': 'Clave actual incorrecta.'}]

    data = {
        'title': 'Perfil',
        'noty': request.session['noty'],
        'user': request.session['user'],
        'profile_form': profile_form,
        'passwd_form': passwd_form
    }
    return render(request, 'dashboard/profile.html', data)


@check_login(1)
@session
def product_seller(request):
    product_form = ProductForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if product_form.is_valid():
            product_form.cleaned_data['vendedor_id'] = request.session['user']['id']
            print(product_form.cleaned_data)
            Producto.objects.create(**product_form.cleaned_data)
            request.session['noty'] = [{'type': 'success', 'msg': 'Producto creado con exito.'}]
        else:
            request.session['noty'] = [{'type': 'error', 'msg': 'Error al crear el producto.'}]
    
    products = Producto.objects.filter(vendedor=request.session['user']['id'])
    data = {
        'title': 'Mis Productos',
        'noty': request.session['noty'],
        'user': request.session['user'],
        'productos': list(products.values()),
        'product_form': product_form
    }
    return render(request, 'dashboard/product.html', data)


@check_login(1)
@session
def product_edit(request, id):
    form = ProductForm(request.POST or None, request.FILES or None, instance=Producto.objects.get(pk=id))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            request.session['noty'] = [{'type': 'success', 'msg': 'Producto actualizado con exito.'}]
        else:
            request.session['noty'] = [{'type': 'error', 'msg': 'Error al actualizar el producto.'}]
    data = {
        'title': 'Editar Producto',
        'noty': request.session['noty'],
        'user': request.session['user'],
        'product_form': form
    }
    return render(request, 'dashboard/product-edit.html', data)

@check_login(1)
def product_remove(request, id):
    try:
        product = Producto.objects.get(pk=id)
        product.delete()
        request.session['noty'] = [{'type': 'success', 'msg': 'Producto eliminado con exito.'}]
    except:
        request.session['noty'] = [{'type': 'error', 'msg': 'Error al eliminar el producto.'}]
    return redirect('products')

