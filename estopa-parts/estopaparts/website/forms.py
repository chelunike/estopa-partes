from django import forms

class RegisterForm(forms.Form):
    TIPOS = ((2, 'Comprador'),(1, 'Vendedor'))

    nif = forms.CharField(max_length=9)
    nombre = forms.CharField(max_length=255)
    apellidos = forms.CharField(max_length=255, required=False)
    correo = forms.EmailField()
    clave = forms.CharField(label='Contraseña', max_length=255)
    tipo = forms.ChoiceField(label='Tipo' ,choices=TIPOS)