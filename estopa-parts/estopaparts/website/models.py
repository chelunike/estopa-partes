from django.db import models

# Create your models here.


class Usuario(models.Model):
    nif = models.CharField(max_length=9)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    correo = models.EmailField()
    clave = models.CharField(max_length=255)
    tipo = models.IntegerField() # 0: Administrador, 1:Vendedor, 2: Cliente

    def __str__(self):
        return self.nombre + ' ' + self.apellidos

class Comprador(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.idUsuario.nombre + ' ' + self.idUsuario.apellidos

class Vendedor(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.idUsuario.nombre + ' ' + self.idUsuario.apellidos

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='products')
    oferta = models.FloatField()
    marca = models.CharField(max_length=255)
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def getPrecio(self):
        if self.oferta > 0:
            return self.precio-(self.precio*(self.oferta*0.01))
        else:
            return self.precio

    def __str__(self):
        return self.nombre


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

    def __str__(self):
        return self.idProducto.nombre


