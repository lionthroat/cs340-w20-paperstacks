from flask import Flask, render_template

from bookData import Books
from genreData import Genres

app = Flask(__name__)

# Save the return value of Books and Genres to new lists variables
Books = Books()
Genres = Genres()

# first route for homepage
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/genres')
def genres():
    return render_template('genres.html', genres=Genres, books=Books)

@app.route('/genre/<string:id>/')
def genre(id):
    return render_template('genre.html', id=int(id), genres=Genres, books=Books)

@app.route('/books')
def books():
    return render_template('books.html', books=Books)

@app.route('/book/<string:id>/')
def book(id):
    return render_template('book.html', id=id, book=Books[int(id)-1]) # I did some fancy bullshit and it worked??

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.errorhandler(404)
def error(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
