from django.db import models

# Create your models here.


class Usuario(models.Model):

    nif = models.CharField(max_length=9)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    correo = models.EmailField()
    clave = models.CharField(max_length=255)
    tipo = models.IntegerField()


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    cantidad = models.IntegerField()
    imagen = models.ImageField()
    oferta = models.FloatField()
    marca = models.CharField(max_length=255)
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Valoracion(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idComprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    valoracion = models.ImageField()


class Pedido(models.Model):
    idComprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaCompra = models.DateField()


class ProductosPedido(models.Model):
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.IntegerField()


