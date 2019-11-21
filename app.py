#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, BuscarForm


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
            pais = formulario.buscar.data
            with open("clientes.csv", encoding="utf8") as archivo:
                archivo_csv = csv.DictReader(archivo)
                paises = []
                for item in archivo_csv:
                    if pais in item["País"]:
                        paises.append(item["País"])
                return render_template("busqueda.html", form=formulario, paises=paises)
        return render_template("busqueda.html", form=formulario)
    return redirect(url_for("ingresar"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
