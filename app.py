#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, BuscarForm, ClienteForm


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido')
                    session['username'] = formulario.usuario.data
                    return render_template('ingresado.html')
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.usuario.data, formulario.password.data]
                archivo_csv.writerow(registro)
            flash('Usuario creado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las passwords no matchean')
    return render_template('registrar.html', form=formulario)


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))


@app.route("/clientes")
def clientes():
    if "username" in session:
        with open("clientes.csv", encoding="utf8") as archivo:
            archivo_csv = csv.DictReader(archivo)
            headers = next(archivo_csv)
            personas = []
            for row in archivo_csv:
                personas.append(row)
        return render_template("clientes.html", headers=headers, personas=personas, cantidad=len(personas))
    else:
        return redirect(url_for("ingresar"))


@app.route("/clientes/pais", methods=["GET", "POST"])
def busqueda_por_pais():
    if "username" in session:
        formulario = BuscarForm()
        if formulario.validate_on_submit():#si hice post me envia los datos y sino me renderiza el formulario
            pais = formulario.buscar.data.capitalize()
            with open("clientes.csv", encoding="utf8") as archivo:
                archivo_csv = csv.DictReader(archivo)
                paises = []
                for item in archivo_csv:
                    if pais in item["País"] and item["País"] not in paises:
                        paises.append(item["País"])
                if not paises:
                    flash('No se encontraron clientes')
                return render_template("busqueda.html", form=formulario, paises=paises)
        return render_template("busqueda.html", form=formulario)
    return redirect(url_for("ingresar"))


@app.route("/clientes/<string:pais>")
def clientes_pais(pais:str):
    if "username" in session:
        with open("clientes.csv", encoding="utf8") as archivo:
            archivo_csv = csv.DictReader(archivo)
            headers = next(archivo_csv)
            clientes = []
            for cliente in archivo_csv:
                if cliente["País"] == pais:
                    clientes.append(cliente)
            return render_template("clientes_pais.html", clientes=clientes, headers=headers, cantidad=len(clientes))
    return redirect(url_for("ingresar"))


@app.route("/agregar_cliente", methods=['GET', 'POST'])
def agregarCliente():
    if "username" in session:
        formulario = ClienteForm()
        if formulario.validate_on_submit():#si hago post , si envio los datos me los guarda
            with open("clientes.csv", "a+", newline='', encoding="utf8") as archivo:
                archivo_csv = csv.writer(archivo)
                registro = [formulario.nombre.data, formulario.edad.data, formulario.direccion.data,
                    formulario.pais.data, formulario.documento.data, formulario.fecha_alta.data,
                    formulario.email.data, formulario.trabajo.data ]
                archivo_csv.writerow(registro)
                flash('Cliente registrado correctamente')
                return redirect(url_for("agregarCliente"))
        return render_template("agregar_cliente.html", formulario=formulario)
    return redirect(url_for("ingresar"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
