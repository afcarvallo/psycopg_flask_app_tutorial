from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 
 
app = Flask(__name__)


conn = sqlite3.connect('personas.db', check_same_thread=False) # conecta a la BD 
 
@app.route('/')
def Index():
    cur = conn.cursor() # establece la conexion con BD 
    s = "SELECT * FROM personas" # busca todo lo que hay en la tabla 
    cur.execute(s) # ejecuta la consulta 
    list_users = cur.fetchall() # esta variable se la paso a index.html para hacer un for loop por los resultados de la consulta 
    return render_template('index.html', list_users = list_users) # envia resultado en forma de lista a index.html 
 
@app.route('/add_persona', methods=['POST'])
def add_persona():
    cur = conn.cursor() # establece conexion con la BD 

    # agrega nuevos datos al formulario 
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']

        print(nombre, apellido, email)
 
        # inserta elementos ingresados en el formulario en inddex.html 
        cur.execute("""INSERT INTO personas (rut, nombre, apellido, mail) VALUES (?,?,?,?)""", (rut, nombre, apellido, email)) 

        conn.commit() # hace efectivos los cambios en la BD 

        return redirect(url_for('Index'))

 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_person(id):

    cur = conn.cursor() # establece conexion con la BD 

    # quita elementos que tengan ese id en la tabla 
    cur.execute('DELETE FROM personas WHERE rut = {0}'.format(id)) 
    
    conn.commit() # hace efectivos los cambios en la BD 

    # envia la instruccion a index.html para quitar ese registro de la tabla en la pagina web 
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)





