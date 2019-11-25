from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class SaludarForm(FlaskForm):
    usuario = StringField('Nombre: ', validators=[Required()])
    enviar = SubmitField('Saludar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')


class BuscarForm(FlaskForm):
    buscar = StringField('Búsqueda:', validators=[Required()])
    enviar = SubmitField('Buscar')


class ClienteForm(FlaskForm):
    nombre = StringField("Nombre:", validators=[Required()])
    edad = DecimalField("Edad:", validators=[Required()])
    direccion = StringField("Dirección:", validators=[Required()])
    pais = StringField("País:", validators=[Required()])
    documento = StringField("Documento:", validators=[Required()])
    fecha_alta = DateField("Fecha Alta:", validators=[Required()], format='%Y-%m-%d')
    email = StringField("Correo Electrónico:", validators=[Required()])
    trabajo = StringField("Trabajo:", validators=[Required()])
    enviar = SubmitField("Nuevo Cliente")