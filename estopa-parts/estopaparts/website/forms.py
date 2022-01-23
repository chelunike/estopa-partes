from calendar import weekday
from django import forms
from .models import Usuario, Producto, Valoracion
from django.core.validators import MaxValueValidator, MinValueValidator

class RegisterForm(forms.Form):
    class Meta:
        model = Usuario
        fields = ['nif', 'nombre', 'apellidos', 'correo', 'imagen']
    
    TIPOS = ((2, 'Comprador'),(1, 'Vendedor'))

    clave = forms.CharField(label='Contraseña', max_length=255)
    tipo = forms.ChoiceField(label='Tipo', choices=TIPOS)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nif', 'nombre', 'apellidos', 'correo', 'imagen']


class EmailForm(forms.Form):
    correo = forms.EmailField()

class PasswordForm(forms.Form):
    claveAntigua = forms.CharField(label='Contraseña antigua', widget=forms.PasswordInput, max_length=255)
    clave = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput, max_length=255)
    clave2 = forms.CharField(label='Repita Contraseña', widget=forms.PasswordInput, max_length=255)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad', 'imagen', 'oferta', 'marca'] 


class PayForm(forms.Form):
    numero = forms.IntegerField(label='Número de Tarjeta', validators=[MinValueValidator(1000000000000000), MaxValueValidator(9999999999999999)])
    clave = forms.DateField(label='Fecha de caducidad', widget=forms.SelectDateWidget(years=range(2020, 2030)))
    clave2 = forms.IntegerField(label='Código CVV', widget=forms.PasswordInput, validators=[MinValueValidator(100), MaxValueValidator(999)])


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['titulo', 'comentario', 'valoracion']
    
    idProducto_id = forms.IntegerField(widget=forms.HiddenInput())
    idComprador_id = forms.IntegerField(widget=forms.HiddenInput())
    


