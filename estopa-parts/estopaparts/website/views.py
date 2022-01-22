from errno import EMLINK
import imp
import re

import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict

from .models import *
from .forms import *

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
        if 'carrito' not in request.session:
            request.session['carrito'] = []
        if 'filtro' not in request.session:
            request.session['filtro'] = {}
        
        result = func(request, *args, **kwargs)
        # Clean norifications
        request.session['noty'] = []
        return result
    return wrapper


# Create your views here.
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
    del request.session['carrito']
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
    articulos = 0
    for p in request.session['carrito']:
        articulos+=1
    minPrice=Producto.objects.raw('SELECT * FROM website_producto ORDER BY precio ASC limit 1;')[0]
    maxPrice=Producto.objects.raw('SELECT * FROM website_producto ORDER BY precio DESC limit 1;')[0]
    print(minPrice.precio)
    print(maxPrice.precio)
    data = {
        'productos': Producto.objects.all(),
        "carrito": request.session['carrito'],
        "web": "productos",
        "id": id,
        "articulos":articulos,
        "minPrice": minPrice.precio,
        "maxPrice": maxPrice.precio,
        "limInf":minPrice.precio,
        "limSup":maxPrice.precio,
        "marcas":list(Producto.objects.all().values_list('marca', flat=True).distinct())

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
                data["articulos"]=articulos-1
                return render(request, 'website/carrito.html', data)
        if value=='filtrarPrecio':
            data['productos']=Producto.objects.raw("SELECT * FROM website_producto WHERE precio BETWEEN "+ request.POST['precioMin'] +" AND "+ request.POST['precioMax']+";")
            data['limInf']=request.POST['precioMin']
            data['limSup']=request.POST['precioMax']
            request.session.modified = True
        if value=='filtrarMarca':
            data['productos']=Producto.objects.raw("SELECT * FROM website_producto WHERE precio BETWEEN "+ request.POST['precioMin'] +" AND "+ request.POST['precioMax']+";")
            data['limInf']=request.POST['precioMin']
            data['limSup']=request.POST['precioMax']
            request.session.modified = True
    for p in request.session['carrito']:
        id.append(p['id'])
    
    return render(request, 'website/mostrar-productos.html', data)

@session
def carrito(request):
    final = 0
    total = 0
    descuento = 0
    articulos = 0
    for p in request.session['carrito']:
        articulos+=1
        producto =  Producto.objects.get(pk=p['id'])
        total += producto.precio
        final += producto.getPrecio()

    descuento = final - total
    data = {
        "carrito": request.session['carrito'],
        "web": "carrito",
        "final":final,
        "total":total,
        "descuento":descuento,
        "articulos":articulos
    }

    return render(request, 'website/carrito.html', data)

@session
def compra(request):
    final = 0
    total = 0
    descuento = 0
    articulos = 0
    cantidad=0
    comprados=[]   
    if request.method == 'POST':
        value=request.POST['submit']
        if value=="solo":
            producto =  Producto.objects.get(pk=request.POST['id'])
            print(producto)
            total += producto.precio
            final += producto.getPrecio()
            cantidad=request.POST['cantidad_'+str(request.POST['id'])]
            producto.cantidad=cantidad
            total*=int(cantidad)
            final*=int(cantidad)
            comprados.append(producto)
            articulos+=1
        if value=="todos":
            for p in request.session['carrito']:
                producto =  Producto.objects.get(pk=p['id'])
                cantidad=request.POST['producto_id_'+str(p['id'])]
                articulos+=1
                producto.cantidad=cantidad
                comprados.append(producto)
                total += (producto.precio*int(cantidad))
                final += (producto.getPrecio()*int(cantidad))
    descuento = final - total            
    
    data = {
        "comprados":comprados,
        "carrito": request.session['carrito'],
        "web": "compra",
        "final":final,
        "total":total,
        "descuento":descuento,
        "articulos":articulos
    }
    return render(request, 'website/compra.html', data)

@check_login(2)
@session
def tramitar(request):
    if len(request.session['carrito'])==0:
        return redirect('home')
    if request.method == 'POST':
        pedido = {
            'idComprador': Usuario.objects.get(pk=request.session['user']['id']),
            'fechaCompra': datetime.datetime.now()
        }
        p = Pedido.objects.create(**pedido)
    
        for name, value in request.POST.items():
            if name.startswith('id_'):
                productosPedidos = {
                    'idProducto': Producto.objects.get(pk=value),
                    'cantidad': request.POST['cantidad_'+str(value)],
                    'estado': 0,
                    'idPedido': Pedido.objects.get(pk=p.id)
                }
                ProductosPedido.objects.create(**productosPedidos)
    request.session['carrito'] = []
    data = {
        'noty': request.session['noty']
    }
    return redirect('home')

@check_login(2)
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
    email_form = EmailForm(request.POST or None)

    if request.method == 'POST':
        if profile_form.is_valid(): # -- -- Datos del Usuario -- --
            profile_form.save()
            request.session['noty'] = [{'type': 'success', 'msg': 'Datos actualizados con exito.'}]
            request.session['user'].update(profile_form.cleaned_data)
            request.session.modified = True
        elif passwd_form.is_valid(): # -- -- Contraseña -- --
            usuario = Usuario.objects.get(pk=request.session['user']['id'])
            if check_password(passwd_form.cleaned_data['claveAntigua'], usuario.clave):
                usuario.clave = make_password(passwd_form.cleaned_data['clave'])
                usuario.save()
                request.session['noty'] = [{'type': 'success', 'msg': 'Clave actualizada con exito.'}]
            else:
                request.session['noty'] = [{'type': 'error', 'msg': 'Clave actual incorrecta.'}]
        elif email_form.is_valid() and 'action' in request.POST: # -- -- Darse de Baja -- --
            usuario = Usuario.objects.get(pk=request.session['user']['id'])
            if usuario.correo == email_form.cleaned_data['correo0'] and request.POST['action'] == 'borrar':
                request.session['noty'] = [{'type': 'success', 'msg': 'Usuario eliminado correctamente.'}]
                usuario.delete()
                del request.session['user']
                return redirect('home')
            else:
                request.session['noty'] = [{'type': 'error', 'msg': 'Error al darse de baja el correo no coincide.'}]

    data = {
        'title': 'Perfil',
        'noty': request.session['noty'],
        'user': request.session['user'],
        'profile_form': profile_form,
        'passwd_form': passwd_form,
        'quit_form': email_form,
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


@check_login(2)
@session
def products_list(request):
    if request.session['user']['tipo'] == 1:
        title = 'Productos vendidos'
        products = Producto.objects.raw('SELECT * FROM website_producto '+
        ' WHERE vendedor_id = %s and id in (select idProducto_id from website_productospedido)',
         [request.session['user']['id']])
    elif request.session['user']['tipo'] == 2:
        title = 'Productos Comprados'
        products = Producto.objects.raw('SELECT * FROM website_producto as prod, website_pedido as ped, website_productospedido as pp '+
            'WHERE prod.id = pp.idProducto_id and ped.id = pp.idPedido_id and ped.idComprador_id = %s;', [request.session['user']['id']])

    data = {
        'title': title,
        'productos': products,
        'noty': request.session['noty'],
        'user': request.session['user'],
    }
    return render(request, 'dashboard/list-products.html', data)

@session
def product_single(request, id):

    if request.method == 'POST' and 'id' in request.POST and 'action' in request.POST:
        if request.POST['action'] == 'insert':
            producto =  model_to_dict(Producto.objects.get(pk=request.POST['id']))
            producto['imagen'] = str(producto['imagen'])
            request.session['carrito'].append(producto)
            request.session.modified = True
        elif request.POST['action'] == 'delete':
            i=0
            for producto in request.session['carrito']:
                if producto['id'] == int(request.POST['id']):
                    del request.session['carrito'][i]
                    request.session.modified = True
                    break
                i+=1
    ids = []
    for p in request.session['carrito']:
        ids.append(p['id'])

    data = {
        'title': 'Producto',
        'noty': request.session['noty'],
        'producto': Producto.objects.get(pk=id),
        'ids': ids,
    }

    return render(request, 'website/product.html', data)

@check_login(2)
@session
def orders(request):
    if request.method == 'POST' and 'id' in request.POST and 'cantidad' in request.POST:
        try:
            linea = ProductosPedido.objects.get(pk=request.POST['id'])
            if linea.estado == 0:
                linea.cantidad = int(request.POST['cantidad'])
                linea.save()
                request.session['noty'] = [{'type': 'success', 'msg': 'Cantidad actualizada con exito.'}]
            else:
                request.session['noty'] = [{'type': 'error', 'msg': 'No se puede actualizar la cantidad.'}]
        except:
            request.session['noty'] = [{'type': 'error', 'msg': 'Error al actualizar la cantidad.'}]

    pedidos = Pedido.objects.filter(idComprador=request.session['user']['id'])
    pedidos_dict = pedidos.values()
    for i, ped in enumerate(pedidos_dict):
        cantidad = 0
        total = 0
        productos = ProductosPedido.objects.filter(idPedido_id=ped['id'])
        ped['productos'] = productos.values()
        
        for prod in ped['productos']:
            producto = Producto.objects.get(pk=prod['idProducto_id'])
            cantidad += prod['cantidad']
            total += prod['cantidad'] * producto.getPrecio()
            prod['data'] = producto
        ped['cantidad'] = cantidad
        ped['total'] = total
        ped['min_estado'] = pedidos[i].min_estado()
        ped['max_estado'] = pedidos[i].max_estado()
    
    data = {
        'title': 'Mis Pedidos',
        'pedidos': pedidos_dict,
        'noty': request.session['noty'],
        'user': request.session['user'],
    }
    return render(request, 'dashboard/orders.html', data)


@check_login(2)
def order_remove(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
        if pedido.max_estado() < 1:
            pedido.delete()
            request.session['noty'] = [{'type': 'success', 'msg': 'Pedido eliminado con exito.'}]
        else:
            request.session['noty'] = [{'type': 'error', 'msg': 'No se puede modificar el pedido.'}]
    except:
        request.session['noty'] = [{'type': 'error', 'msg': 'Error al eliminar el pedido.'}]
    return redirect('orders')

@check_login(2)
def order_remove_product(request, order_id, product_id):
    try:
        producto = ProductosPedido.objects.get(idPedido=order_id, idProducto=product_id)
        if producto.estado < 1:
            producto.delete()
            request.session['noty'] = [{'type': 'success', 'msg': 'Producto del pedido eliminado con exito.'}]
        else:
            request.session['noty'] = [{'type': 'error', 'msg': 'No se puede modificar el Producto del pedido.'}]
    except:
        request.session['noty'] = [{'type': 'error', 'msg': 'Error al eliminar el Producto del pedido.'}]
    return redirect('orders')


