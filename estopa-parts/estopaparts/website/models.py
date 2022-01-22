from re import T
from django.db import models


# Create your models here.
class Usuario(models.Model):
    TIPOS = {
        ('0', 'Administrador'),
        ('1', 'Vendedor'),
        ('2', 'Comprador'),
    }

    nif = models.CharField(max_length=9)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    correo = models.EmailField()
    clave = models.CharField(max_length=255)
    tipo = models.IntegerField(choices=TIPOS) # 0: Administrador, 1:Vendedor, 2: Cliente

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
    imagen = models.ImageField(upload_to='products', null=True, blank=True)
    oferta = models.FloatField()
    marca = models.CharField(max_length=255)
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def getPrecio(self):
        if self.oferta > 0:
            return self.precio-(self.precio*(self.oferta*0.01))
        else:
            return self.precio

    def __str__(self):
        return "Id: " + str(self.id) + " Nombre: "+self.nombre+", \n "+"Descripcion: "+self.descripcion + \
            ", \n"+"Precio: "+str(self.precio)+", \n"+"cantidad: "+str(self.cantidad)+", \n"+", \n"+"oferta: "+str(self.oferta)+", \n"+"marca: "+str(self.marca)


class Valoracion(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idComprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    valoracion = models.ImageField()


class Pedido(models.Model):
    idComprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fechaCompra = models.DateField()

    def get_total(self):
        total = 0
        for linea in ProductosPedido.objects.filter(idPedido=self.id):
            total += linea.get_precio()
        return total
    
    def min_estado(self):
        estado = 10
        for linea in ProductosPedido.objects.filter(idPedido=self.id):
            if estado > linea.estado:
                estado = linea.estado
        return estado
    
    def max_estado(self):
        estado = 0
        for linea in ProductosPedido.objects.filter(idPedido=self.id):
            if estado <= linea.estado:
                estado = linea.estado
        return estado

    def __str__(self):
        return "Id: " + str(self.id) + " Comprador: "+self.idComprador.nombre+", \n "+"Fecha: "+str(self.fechaCompra)


class ProductosPedido(models.Model):
    ESTADOS = {
        (0, 'Pendiente'),
        (1, 'Confirmado'),
        (2, 'Pagado'),
        (3, 'Enviado'),
        (4, 'Recibido'),
    }

    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.IntegerField(choices=ESTADOS, default=0)

    def get_precio(self):
        return (self.idProducto.getPrecio()*self.cantidad)

    def __str__(self):
        return self.idProducto.nombre


