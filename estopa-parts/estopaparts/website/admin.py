from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Valoracion)
admin.site.register(Pedido)
admin.site.register(ProductosPedido)

