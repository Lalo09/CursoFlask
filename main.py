from flask import Flask,redirect, url_for, render_template,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'

#Conexion a base de datos
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='proyectoflask'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')
"""Ruta con parametros
@app.route('/informacion/<string:texto>')
def informacion(texto):
    return render_template('informacion.html',texto=texto)
"""

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
"""Redireccion
@app.route('/contacto/<redireccion>')
def contacto(redireccion = None):

    if redireccion != None:
        return redirect(url_for('lenguajes'))

    return "<h1>Pagina de contacto </h1>"
"""

@app.route('/lenguajes-de-programacion')
def lenguajes():
    return render_template('lenguajes.html')

@app.route('/crear-coche',methods=['GET','POST'])
def crear_coche():
    
    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches VALUES (null,%s,%s,%s,%s)",(marca,modelo,precio,ciudad))
        cursor.connection.commit()

        flash('Coche agregado correctamente')

        return redirect(url_for('index'))        

    return render_template('crear_coche.html')
    
@app.route('/coches')
def coches():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches ORDER BY id DESC")
    coches = cursor.fetchall()
    cursor.close()

    return render_template('coches.html',coches=coches)

@app.route('/coche/<coche_id>')
def coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s",(coche_id))
    coche = cursor.fetchall()
    cursor.close()

    return render_template('coche.html',coche=coche[0])

@app.route('/borrar-coche/<coche_id>')
def borrar_coche(coche_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM coches WHERE id = %s",(coche_id))
    mysql.connection.commit()

    flash('Coche eliminado correctamente')

    return redirect(url_for('coches'))

@app.route('/editar-coche/<coche_id>',methods=['GET','POST'])
def editar_coche(coche_id):

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE coches
            SET marca = %s,
                modelo = %s,
                precio = %s,
                ciudad = %s
                WHERE id = %s
        """,(marca,modelo,precio,ciudad,coche_id))
        cursor.connection.commit()

        flash('Coche editado correctamente')

        return redirect(url_for('coches'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM coches WHERE id = %s",(coche_id))
    coche = cursor.fetchall()
    cursor.close()

    return render_template('crear_coche.html',coche=coche[0])

if __name__ == '__main__':
    app.run(debug=True)