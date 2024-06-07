from flask import Blueprint, request
from flask_restful import Api, Resource
from .db import get_db, close_db

api_bp = Blueprint('api', __name__, url_prefix='/api/books')
api = Api(api_bp)

class BookResource(Resource):
    def get_all_books(self):
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM Tb_libros")
        books = c.fetchall()
        close_db(db)
        return books

    def get_book_by_id(self, book_id):
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM Tb_libros WHERE cod_libro = ?", (book_id,))
        book = c.fetchone()
        if book:
            return book
        else:
            return {'error': 'Libro no encontrado'}, 404

    def get(self, book_id=None):
        if book_id:
            return self.get_book_by_id(book_id)
        else:
            return self.get_all_books()

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

api.add_resource(BookResource, '/', '/<int:book_id>')
