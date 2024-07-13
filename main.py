from flask import Flask, request, render_template, redirect, url_for
import requests
from .routes import api_bp
from .db import get_db, close_db

app = Flask(__name__)
app.register_blueprint(api_bp)

# Ruta para el Index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filters = {
            'book_id': request.form.get('book_id'),
            'name': request.form.get('name'),
            'author': request.form.get('author'),
            'year': request.form.get('year'),
            'genre': request.form.get('genre')
        }
        # Print the filters to debug
        print(f"Filters from form: {filters}")
        try:
            response = requests.get('http://127.0.0.1:5000/api/books', params=filters)
            response.raise_for_status()
            books = response.json()
            return render_template('index.html', books=books)
        except requests.exceptions.RequestException as e:
            return render_template('index.html', error=str(e))
    else:
        try:
            response = requests.get('http://127.0.0.1:5000/api/books')
            response.raise_for_status()
            books = response.json()
            return render_template('index.html', books=books)
        except requests.exceptions.RequestException as e:
            return render_template('index.html', error=str(e))


# Ruta para el Formulario de un Nuevo Libro
@app.route('/formulario', methods=['GET' ,'POST'])
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

# Ruta para Actualizar un Libro
@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update(book_id):
    # Obtenemos los datos del libro a actualizar de la API REST
    response = requests.get(f'http://127.0.0.1:5000/api/books/{book_id}')
    book = response.json()
    print(book)
    
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

@app.route('/delete/<book_id>')
def delete(book_id):
        # Eliminamos el libro de la API REST
        response = requests.delete(f'http://127.0.0.1:5000/api/books/{book_id}')
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return render_template('delete.html', book_id=book_id, error=response.json()['message'])
        

if __name__ == '__main__':
    app.run(debug=True)