## Inicialización del Proyecto

- Tener instalado Python la ultima versión para no tener complicaciones al desarrollar el proyecto
- Empezaremos abriendo nuestra consola de comandos, más factible que sea en modo administrador, creamos una nueva carpeta donde estará el proyecto a desarrollar y nos redireccionaremos a la carpeta creada posteriormente

> mkdir myproject

> cd myproject

- Estando dentro de la carpeta creamos un entorno virtual con el siguiente comando

> py -3 -m venv .venv

- Ya teniendo instalado nuestro entorno virtual, activaremos de la siguiente manera

> .\env\Scripts\activate

- Luego de aquello instalaremos nuestro Framework de Python que en este caso será Flask

> pip install flask

- En el caso que nos pida tener que actualizar nuestro pip, solamente ejecutaremos

pip install --upgrade pip

## Ruta de los Archivos
1. Dentro de la carpeta "App" tiene los siguientes archivos:
1.1. _init_.py: Este archivo realiza la inicialización del proyecto
1.2. db.py: Tenemos la conexión de la base de datos que está realizada con SQLite3
1.3. main.py: Es donde se ejecuta toda la aplicacion web con sus rutas específicas
1.4. routes.py: Tenemos la realización de los procesos CRUD mediante la API-RESTFUL

## API - RESTFULL
### Metodo Get
Mediante el método Get se realizó la consulta para traer todos los datos e información de la base de datos

    def get_all_books(self):
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM Tb_libros")
        books = c.fetchall()
        close_db(db)
        return books

Realizamos otra función donde nos va permitir realizar la búsqueda por el identificador de la tabla.

    def get_book_by_id(self, book_id):
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM Tb_libros WHERE cod_libro = ?", (book_id,))
        book = c.fetchone()
        if book:
            return book
        else:
            return {'error': 'Libro no encontrado'}, 404

### Método POST
Para poder hacer el envio o registro de una nueva información, realizamos una función que nos permita realizar aquella acción mediante el método POST

    def post(self):
        db = get_db()
        c = db.cursor()
        data = request.get_json()
        if not data or 'titulo' not in data or 'autor' not in data or 'genero' not in data or 'anio_publicacion' not in data:
            return {'message': 'Datos incompletos'}, 400
        try:
            c.execute("INSERT INTO Tb_libros (titulo, autor, genero, anio_publicacion) VALUES (?, ?, ?, ?)",
                      (data['titulo'], data['autor'], data['genero'], data['anio_publicacion']))
            db.commit()
        except Exception as e:
            return {'message': 'Error al crear el libro', 'error': str(e)}, 500
        close_db(db)
        return {'message': 'Libro creado exitosamente'}, 201

### Método PUT
Para la actualización de los datos también se aplicó una función que nos permita tal acción consultando por su identificador

    def put(self, book_id):
        db = get_db()
        c = db.cursor()
        data = request.get_json()
        if not data or 'titulo' not in data or 'autor' not in data or 'genero' not in data or 'anio_publicacion' not in data:
            return {'message': 'Datos incompletos'}, 400
        try:
            c.execute("UPDATE Tb_libros SET titulo = ?, autor = ?, genero = ?, anio_publicacion = ? WHERE cod_libro = ?",
                      (data['titulo'], data['autor'], data['genero'], data['anio_publicacion'], book_id))
            if c.rowcount == 0:
                return {'message': 'Libro no encontrado'}, 404
            db.commit()
        except Exception as e:
            return {'message': 'Error al actualizar el libro', 'error': str(e)}, 500
        close_db(db)
        return {'message': 'Libro actualizado exitosamente'}, 200

### Método DELETE
El siguiente proceso del CRUD es el método DELETE que nos permitirá eliminar cada registro comprobando por su identificador

    def delete(self, book_id):
        db = get_db()
        c = db.cursor()
        try:
            c.execute("DELETE FROM Tb_libros WHERE cod_libro = ?", (book_id,))
            if c.rowcount == 0:
                return {'message': 'Libro no encontrado'}, 404
            db.commit()
        except Exception as e:
            return {'message': 'Error al eliminar el libro', 'error': str(e)}, 500
        close_db(db)
        return {'message': 'Libro eliminado exitosamente'}, 200

### RUTA API
Para configurar la ruta de la API, agregamos el siguiente codigo que nos permite comprobar la API mediante Postman

	api_bp = Blueprint('api', _name_, url_prefix='/api/books')
	api = Api(api_bp)
	api.add_resource(BookResource, '/', '/<int:book_id>')

- Ruta de la API GET
http://127.0.0.1:5000/api/books

- Ruta de la API GET por ID
http://127.0.0.1:5000/api/books/id

- Ruta de la API POST
http://127.0.0.1:5000/api/books

- Ruta de la API PUT
http://127.0.0.1:5000/api/books/id

- Ruta de la API DELETE
http://127.0.0.1:5000/api/books/id

### Ejecución del Programa
Para ejecutar correctamente el programa, primeramente debemos crear una carpeta llamada "Templates" donde estará nuestra Aplicación Web, aqui estarán los archivos
1. base.html
2. index.html
3. formulario.html
4. update.html

Estos 4 archivos nos permitirá visualizar la información de manera correcta

Además en nuestro archivo main.py, vincularemos nuestras rutas de la API-REST para hacer uso de ellas

* Ruta para el Index.html
Empezamos creando una ruta con sus métodos tanto GET como POST para traer los parametros y hacer la búsqueda por identificador

		@app.route('/', methods=['GET', 'POST'])

Seguido de eso creamos una funcion llamada "index()" que consumirá la API REST que hemos creado previamente, aqui incluimos tanto nuestro API que consume todos lo datos y por búsqueda de ID.

	def index():
		if request.method == 'POST':
			book_id = request.form['book_id']
			# Obtener un libro específico desde tu API REST
			response = requests.get(f'http://127.0.0.1:5000/api/books/{book_id}')
			if response.status_code == 200:
				book = response.json()
				return render_template('index.html', book=book)
			else:
				return render_template('index.html', error='Libro no encontrado')
		else:
			# Obtener la lista de libros desde tu API REST
			response = requests.get('http://127.0.0.1:5000/api/books')
			if response.status_code == 200:
				books = response.json()
				return render_template('index.html', books=books)
			else:
				return render_template('index.html', error='Error al obtener los libros')

* Ruta para el Formulario o Registro de un nuevo Libro

Empezamos creando nuestra nueva ruta que en este caso le hemos denominado "/formulario" con sus métodos tanto GET y POST.

		@app.route('/formulario', methods=['GET' ,'POST'])

Creamos una nueva función donde se hará todo el proceso de crear un nuevo registro, con su método respectivo como es el POST, consumiendo de la API REST

		def create():
			if request.method == 'POST':
				#Enviamos los datos del libro a la API REST
				data = {
					'titulo': request.form['titulo'],
					'autor': request.form['autor'],
					'genero': request.form['genero'],
					'anio_publicacion': request.form['anio_publicacion'],
				}
				response = requests.post('http://127.0.0.1:5000/api/books', json=data)

				if response.status_code == 201:
					return redirect(url_for('index'))
				else:
					return render_template('create.html', error=response.json()['message'])
			return render_template('formulario.html')

* Ruta para Actualizar un nuevo registro

Creamos una nueva ruta llamada "/update", pero en este caso llamamos al parametro "ID" para poder hacer la comprobación y actualizar el identificador que el usuario haya seleccionado

		@app.route('/update/<int:book_id>', methods=['GET', 'POST'])

Una vez creada nuestra ruta, procedemos a crear nuestra función llamandole el parámetro de ID que nos permitirá hacer la comprobación y así actualizaremos la información que el usuario haya seleccionado.

		def update(book_id):
			# Obtenemos los datos del libro a actualizar de la API REST
			response = requests.get(f'http://127.0.0.1:5000/api/books/{book_id}')
			book = response.json()

			if request.method == 'POST':
				# Enviamos los datos actualizados del libro a la API REST
				data = {
					'titulo': request.form['titulo'],
					'autor': request.form['autor'],
					'genero': request.form['genero'],
					'anio_publicacion': request.form['anio_publicacion']
				}
				response = requests.put(f'http://127.0.0.1:5000/api/books/{book_id}', json=data)
				if response.status_code == 200:
					return redirect(url_for('index'))
				else:
					return render_template('update.html', book_id=book_id, error=response.json()['message'])

			# Obtenemos los datos del libro a actualizar de la API REST
			response = requests.get(f'http://127.0.0.1:5000/api/books/{book_id}')
			book = response.json()
			return render_template('update.html', book=book, book_id=book_id)

* Ruta para Eliminar un registro

Finalmente tenemos la ultima ruta que nos permitirá eliminar un registro de nuestra base de datos, empezamos creando nuestra ruta

		@app.route('/delete/<book_id>')

Una vez creada nuestra ruta, crearemos una función que nos permita consumir la API y eliminar la información

		def delete(book_id):
			# Eliminamos el libro de la API REST
			response = requests.delete(f'http://127.0.0.1:5000/api/books/{book_id}')
			if response.status_code == 200:
				return redirect(url_for('index'))
			else:
				return render_template('delete.html', book_id=book_id, error=response.json()['message'])
 
 ### Template
 * Visualización de los datos
 
 Para la visualización de los registros realizamos una tabla que iteramos por la posición que se encuentra nuestra base de datos o en este caso como Array
                <td>{{ book[0] }}</td>
                <td>{{ book[1] }}</td>
                <td>{{ book[2] }}</td>
                <td>{{ book[3] }}</td>
                <td>{{ book[4] }}</td>
Si se desea hacer una búsqueda por el identificador, ejecutaremos un condicional que dependiendo del identificador ingresado en el input, se mostrará el identificador deseado, caso contrario se mostrarán todos los datos.
            {% if book %}
            <tr>
                <td>{{ book[0] }}</td>
                <td>{{ book[1] }}</td>
                <td>{{ book[2] }}</td>
                <td>{{ book[3] }}</td>
                <td>{{ book[4] }}</td>
            </tr>
            {% else %}
            {% for book in books %}
            <tr>
                <td>{{ book[0] }}</td>
                <td>{{ book[1] }}</td>
                <td>{{ book[2] }}</td>
                <td>{{ book[3] }}</td>
                <td>{{ book[4] }}</td>
            </tr>
            {% endfor %}
            {% endif %}
 
* Actualizar Informacion

Para poder actualizar una información se ha implementado una etiqueta que nos redireccione a la página para poder editar la información, en este caso al archivo "update.html" que ya hemos definido en nuestro main.py
 
    <a href="/update/{{ book[0] }}" class="btn btn-primary me-2">Editar</a>

* Eliminar Información

Para poder eliminar una información tambien se ha implementado una etiqueta que nos permita realizar tal acción llamando a la función que se ha creado en el main.py

    <a href="/delete/{{ book[0 ]}}" class="btn btn-danger">Eliminar</a>

* Añadir Informacion

Por ultimo para añadir una información se ha creado un nuevo template llamdo "formulario.html" que se registrará toda la información.

    <form action="{{ url_for('create') }}" method="POST" class="form-group">

# Nota
Hay que tener en cuenta que para poder ejecutar un proyecto debemos realizarlo con el comando

> flask --app main.py run

En el caso que se desea ejecutar con el depurador encendido lo podemos hacer de la siguiente manera

>flask --app main.py --debug run

###End
