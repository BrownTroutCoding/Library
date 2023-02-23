from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db,  Book, book_schema, books_schema

api = Blueprint('api',__name__,url_prefix='/api')

# Get Data
@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

# Create
@api.route('/books',methods=['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    year = request.json['year']
    read = request.json['read']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, title, author, year, read, user_token=user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

#Read
@api.route('/books',methods=['GET'])
@token_required
def get_book(current_user_token):
    token = current_user_token.token
    books = Book.query.filter_by(user_token = token).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>',methods=['GET'])
@token_required
def get_single_book(current_user_token,id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

#Update
@api.route('/books/<id>',methods=["POST", "PUT"])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    
    book.title = request.json['title']
    book.author = request.json['author']
    book.year = request.json['year']
    book.read = request.json['read']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

#Delete
@api.route('/books/<id>',methods=["DELETE"])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)