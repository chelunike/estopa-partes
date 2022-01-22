from django import forms
from .models import Usuario, Producto

class RegisterForm(forms.Form):
    TIPOS = ((2, 'Comprador'),(1, 'Vendedor'))

    nif = forms.CharField(max_length=9)
    nombre = forms.CharField(max_length=255)
    apellidos = forms.CharField(max_length=255, required=False)
    correo = forms.EmailField()
    clave = forms.CharField(label='Contraseña', max_length=255)
    tipo = forms.ChoiceField(label='Tipo', choices=TIPOS)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nif', 'nombre', 'apellidos', 'correo']


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

