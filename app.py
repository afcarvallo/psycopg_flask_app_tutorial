from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 , para python3.9 usar pip3 install psycopg2-binary
import psycopg2.extras
 
app = Flask(__name__)

app.secret_key = 'andres1234' # esta secret key permite borrar objetos de la aplicacion 

#antes crear BD , tabla, insertar tuplas de ejemplo y modificar alter sequence para que deje seguir insertando tuplas 
# CREATE TABLE personas (id serial PRIMARY KEY, nombre VARCHAR(40) NOT NULL,apellido VARCHAR(40) NOT NULL, email VARCHAR(40) NOT NULL);
# INSERT INTO personas VALUES ('1', 'Juan', 'Batista', 'mail1@mail.com');
# INSERT INTO personas VALUES ('2', 'Pablo', 'Sergiovich', 'mail2@mail.com');
# INSERT INTO personas VALUES ('3', 'Jimi', 'Elgueta', 'mail3@mail.com');
# INSERT INTO personas VALUES ('4', 'Julio', 'Green', 'mail4@mail.com');
# ALTER SEQUENCE personas_id_seq RESTART WITH 9;

# recordar verificar los permisos para borrar e insertar elementos a la BD 
# \du 
# alter role <user-name> superuser; 
DB_HOST = "localhost" # localhost 
DB_NAME = "mydb" # nombre de la base de datos 
DB_USER = "myuser" # nombre de usuario 
DB_PASS = "mypass" # password 

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) # conecta a la BD 
 
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # establece la conexion con BD 
    s = "SELECT * FROM personas" # busca todo lo que hay en la tabla 
    cur.execute(s) # ejecuta la consulta 
    list_users = cur.fetchall() # esta variable se la paso a index.html para hacer un for loop por los resultados de la consulta 
    return render_template('index.html', list_users = list_users) # envia resultado en forma de lista a index.html 
 
@app.route('/add_persona', methods=['POST'])
def add_persona():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # establece conexion con la BD 

    # agrega nuevos datos al formulario 
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
 
        # inserta elementos ingresados en el formulario en inddex.html 
        cur.execute("INSERT INTO personas (nombre, apellido, email) VALUES (%s,%s,%s)", (nombre, apellido, email)) 

        conn.commit() # hace efectivos los cambios en la BD 

        return redirect(url_for('Index'))

 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_person(id):

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # establece conexion con la BD 

    # quita elementos que tengan ese id en la tabla 
    cur.execute('DELETE FROM personas WHERE id = {0}'.format(id)) 
    
    conn.commit() # hace efectivos los cambios en la BD 

    # envia la instruccion a index.html para quitar ese registro de la tabla en la pagina web 
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)





