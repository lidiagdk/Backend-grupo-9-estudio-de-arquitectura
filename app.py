from multiprocessing import Value
from flask import Flask   #para importar una clase flask
from flask import render_template # metodo p/renderizar templeates
from flask import request #para obtener datos del formulario
from flaskext.mysql import MySQL #importo la clase mysql de la libreria flask para una conexion

baseurl = 'http://127.0.0.1:5500/'
urlback = 'http://127.0.0.1:5000/'

app = Flask(__name__)    #creo la instancia de flask


mysql= MySQL()    #creo la instancia de Mysql y luego se empieza a setear  al objeto de configuracion que es app

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1' #defino el localhost,seteo el localhost
app.config['MYSQL_DATABASE_PORT'] = 3306 #defino el puerto o seteo el puerto

app.config['MYSQL_DATABASE_USER'] ='root'   #defino o seteo usuario
app.config['MYSQL_DATABASE_PASSWORD'] = '3214' #defino o seteo contraseña

app.config['MYSQL_DATABASE_ DB'] ='arq_sustentable' #defino la base de datos

mysql.init_app(app)#iniciando la aplicacion con el metodo init
@app.route('/') #defino la ruta
def index (): #defino la funcion bloque del codigo
    
    sql="SELECT * FROM arq_sustentable.proyectos;" #DEFINO LA CONSULTA
    conn= mysql.connect() #creo la conexion con el metodo connect
    cursor= conn.cursor() #creo un cursor de la base de datos
    cursor.execute(sql) #ejecuto la consulta

    
    data_proyectos = cursor.fetchall() #obtengo los datos de la consulta haciendo un fetch
    cursor.close() #cierro el cursor
    
    return render_template('proyectos/index.html', proyectos=data_proyectos)#retorno el template,renderizamos el template

@app.route('/create') #defino la ruta
def create(): #funcion para renderizar el tempate/html de crear proyectos
    return render_template('proyectos/create.html')

@app.route('/guardar_proyecto', methods=['POST'])

def guardar_proyecto():
      Nombre_proyecto= request.form['Nombre_proyecto']
      Ubicacion= request.form['Ubicacion']
      Inicio_obra= request.form['Inicio_obra']
      Final_obra= request.form['Final_obra']
      Descripcion= request.form['Descripcion']

      sql = "INSERT INTO `arq_sustentable`.`proyectos` (`Nombre_proyecto`, `Ubicacion`, `Inicio obra`, `Final obra`, `Descripcion`) " \
        "VALUES ('" + Nombre_proyecto + "', '" + Ubicacion + "', '" + Inicio_obra + "', '" + Final_obra + "', '" + Descripcion + "')"
      #conn = mysql.get_db().connect()
      conn= mysql.connect()  #conexion a la base de datos
      cursor=conn.cursor()   #cursor de la base de datos
      cursor.execute(sql)    #ejecutamosla consulta
      conn.commit()          #guardamos la consulta
      return "proyecto guardado con exito"

@app.route('/delete/<id>') # creamos la ruta para eliminar 
def delete(id):
     sql="DELETE FROM arq_sustentable.proyectos WHERE id = " + id + ";" #consulta a sql
     conn= mysql.connect()  #conexion a la base de datos
     cursor=conn.cursor()   #cursor de la base de datos
     cursor.execute(sql)    #ejecutamosla consulta
     conn.commit()          #guardamos la consulta
     return "proyecto eliminado con exito"

@app.route('/edit/<id>') #defino la ruta
def edit(id): #funcion para renderizar el tempate/html de crear proyectos
     sql="SELECT * FROM arq_sustentable.proyectos WHERE id=" + id + ";"
     conn= mysql.connect()  #conexion a la base de datos
     cursor=conn.cursor()   #cursor de la base de datos
     cursor.execute(sql)    #ejecutamosla consulta
     data_one_proyecto= cursor.fetchone()
     conn.commit()          #guardamos la consulta
     return render_template('proyectos/edit.html', data_jinja_one_proyecto= data_one_proyecto) # Renderizamos el template

@app.route('/update', methods=['POST'])
def update():
      Nombre_proyecto= request.form['Nombre_proyecto']
      Ubicacion= request.form['Ubicacion']
      Inicio_obra= request.form['Inicio_obra']
      Final_obra= request.form['Final_obra']
      Descripcion= request.form['Descripcion']  


if __name__ == '__main__': #con estas dos ultimas instrucciones simulo correr un servidor,simular un backend local
    app.run(debug=True) #ejecuto la aplicacion en modo debug,ejecutamos el servidor en puerto 3306 de mysql y el 5000 puerto web
