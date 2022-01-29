from flask import Flask, url_for 
from flask import render_template, request, redirect, flash
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = "Desarrollo_juan"       # Llave secreta ya que el servicio esta enviando info a traves de todos los contenidos

mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"]="localhost"
app.config["MYSQL_DATABASE_USER"]="root"
app.config["MYSQL_DATABASE_PASSWORD"]=""
app.config["MYSQL_DATABASE_DB"]="sistema_em"
mysql.init_app(app)              # inicio de la conexion con los datos de la BD



@app.route("/")
def index():
    sql = "SELECT * FROM `empleados`;"
    conexion = mysql.connect()            # Conexion con la inicializacion de la app
    cursor = conexion.cursor()            # lugar donde se almacena lo que se va a ejecutar
    cursor.execute(sql)                   # ejecucion
    empleados = cursor.fetchall()    # Info obtenida, regresa conjuntamente para mostrarla 
    print(empleados)                 # Muestra los registros ya seleccionados
    conexion.commit()                     # la instruccion se termino
    return render_template("empleados/index.html",empleados=empleados)



@app.route("/crear")
def create():                             # Crear informacion de usuarios
    return render_template("empleados/create.html")


@app.route('/guardar', methods=['POST'])
def storage():  
    nombre = request.form["txtNombre"]   
    correo = request.form["txtCorreo"] 
    profesion = request.form["txtProfesion"]
    salario = request.form["txtSalario"]    
    
    if nombre == "" or correo == "" or profesion == "" or salario == "":
        flash("Debes llenar todos los campos")
        return redirect(url_for("create"))
                   
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `profesion`, `salario`) VALUES (NULL, %s, %s, %s, %s);"   # Los valores se acomodaran en el orden que le estoy dando en datos
    datos = (nombre,correo,profesion,salario)
    conexion = mysql.connect()       
    cursor = conexion.cursor()       
    cursor.execute(sql,datos)        
    conexion.commit()     
    return redirect("/")           
#   return render_template("empleados/index.html")



@app.route('/edit/<int:id>')
def edit(id):                         # Edita la informacion
    sql = "SELECT * FROM empleados WHERE id=%s"
    conexion = mysql.connect()       
    cursor = conexion.cursor() 
    cursor.execute(sql,(id))
    empleados = cursor.fetchall()
    print(empleados)
    conexion.commit()
    return render_template("empleados/edit.html", empleados = empleados)


@app.route('/actualizar', methods=['POST'])
def update():
    nombre = request.form["txtNombre"]   
    correo = request.form["txtCorreo"] 
    profesion = request.form["txtProfesion"]
    salario = request.form["txtSalario"] 
    id = request.form["txtId"]
    sql = "UPDATE `empleados` SET `nombre`= %s, `correo` = %s, `profesion` = %s, `salario` = %s WHERE id = %s;"   # Se hace lo mismo que en almacenamiento solo que reescribiendolos
    datos = (nombre,correo,profesion,salario,id)
    conexion = mysql.connect()       
    cursor = conexion.cursor()       
    cursor.execute(sql,datos)        
    conexion.commit()   
    return redirect("/")



@app.route('/destroy/<int:id>')
def delete(id):                     # Elimina el registro
    sql = "DELETE FROM empleados WHERE id=%s"
    conexion = mysql.connect()       
    cursor = conexion.cursor() 
    cursor.execute(sql,(id))      # Elimina todos los empleados cuando encuentre la id que le envian a traves de la url
    conexion.commit()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug = True, port=4114)