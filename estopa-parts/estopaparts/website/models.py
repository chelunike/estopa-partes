from re import T
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Usuario(models.Model):
    TIPOS = [
        (0, 'Administrador'),
        (1, 'Vendedor'),
        (2, 'Comprador'),
    ]
    nif = models.CharField(max_length=9)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    correo = models.EmailField()
    clave = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='users', null=True)
    tipo = models.IntegerField(choices=TIPOS) # 0: Administrador, 1:Vendedor, 2: Cliente
    
    def __str__(self):
        return self.nombre + ' ' + self.apellidos
    def getTipo(self):
        return self.TIPOS[self.tipo][1]

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
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    imagen = models.ImageField(upload_to='products', null=True)
    oferta = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marca = models.CharField(max_length=255)
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def getPrecio(self):
        if self.oferta > 0:
            return self.precio-(self.precio*(self.oferta*0.01))
        else:
            return self.precio

    def calcularMedia(self):
        v = Valoracion.objects.filter(idProducto_id=self.id)
        suma = 0
        for i in v:
            suma += i.valoracion
        if len(v) == 0:
            return 0
        return suma/len(v)

    def __str__(self):
        return "Id: " + str(self.id) + " Nombre: "+self.nombre+", \n "+"Descripcion: "+self.descripcion + \
            ", \n"+"Precio: "+str(self.precio)+", \n"+"cantidad: "+str(self.cantidad)+", \n"+", \n"+"oferta: "+str(self.oferta)+", \n"+"marca: "+str(self.marca)


class Valoracion(models.Model):
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    idComprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    comentario = models.TextField()
    valoracion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def getEstrellas(self):
        estrellas = 'a'*int(self.valoracion//2)
        if self.valoracion % 2 != 0:
            estrellas += 'b'
        else:
            estrellas += 'c'
        estrellas += 'c'*int(4-self.valoracion//2)
        return estrellas
    
    def __str__(self):
        return self.idComprador.nombre + ' ' + self.idProducto.nombre + ' ' + self.titulo + ' ' + self.comentario + ' ' + str(self.valoracion)



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

    def getMes(self):
        return self.fechaCompra.month
        

    def __str__(self):
        return "Id: " + str(self.id) + " Comprador: "+self.idComprador.nombre+", \n "+"Fecha: "+str(self.fechaCompra)


class ProductosPedido(models.Model):
    ESTADOS = [
        (0, 'Pendiente'),
        (1, 'Confirmado'),
        (2, 'Pagado'),
        (3, 'Enviado'),
        (4, 'Recibido'),
    ]

    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.IntegerField(choices=ESTADOS, default=0)

    def get_precio(self):
        return (self.idProducto.getPrecio()*self.cantidad)

    def __str__(self):
        return self.idProducto.nombre


