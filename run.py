import io
import time
import csv
import pymysql
import pymysql.cursors
from app import app
from db import mysql
from flask import Flask, Response, render_template
from flask import request, redirect

@app.route('/')
def index():
    # query 1: get genre data for left sidebar links
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre order by genre.genre_name;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # query 2: get featured book data (NOTE: maybe there is a way to randomize this?)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_book = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id WHERE book.book_title = 'Electric Arches';"
    cursor.execute(select_book)
    featuredBookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('home.html', genres=GenresSQL, featuredbooks=featuredBookSQL)

@app.route('/books')
def books():
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id group by book.isbn order by book.book_title ASC;"
    # Note: groups by isbn so books with multiple authors only display once, however, only one author is shown.
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('books.html', books=result)

@app.route('/book/<string:isbn>/')
def book(isbn):
    # Fetch Book's information
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
	cursor.execute(select_stmt)
	BookSQL = cursor.fetchall()
	cursor.close()
	connection.close()

    # Fetch Book's Ratings and Reviews
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = book.isbn where book.isbn = " + isbn
	cursor.execute(select_stmt)
	ReviewSQL = cursor.fetchall()
	cursor.close()
	connection.close()

	return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL)

@app.route('/add_book', methods=['POST','GET'])
def add_book():
    if request.method == 'GET':
        # Get Genres information
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
        cursor.execute(select_stmt)
        GenresSQL = cursor.fetchall()
        cursor.close()
        connection.close()

        # Get Current Authors information
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select auth.author_id, auth.author_name from Authors auth;"
        cursor.execute(select_stmt)
        AuthorsSQL = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_book.html', genres=GenresSQL, authors=AuthorsSQL)

    elif request.method == 'POST':
        # Operation 1: Fetch Book information from form
        book_title = request.form['book_title']
        isbn = request.form['book_isbn']
        year_published = request.form['book_year']
        book_description = request.form['book_description']
        genres = request.form.getlist('book_genre')
        author_ids = request.form.getlist('book_author')

        # Operation 2: Insert new Book
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Books (isbn, book_title, year_published, book_description) VALUES (%s,%s,%s,%s)'
        values = (isbn, book_title, year_published, book_description)
        print("Values to be inserted to Book are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        # Operation 3: If needed, insert one or more Books_Authors entries
        for author_id in author_ids:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
            values = (isbn, author_id)
            print("Values to be inserted to Books_Authors are: ", values)
            cursor.execute(query, values)
            connection.commit() # NOTE: entry will not be inserted w/o this
            cursor.close()
            connection.close()

        # Operation 4: Insert one or more Genres_Books entries
        for genre_id in genres:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = 'INSERT INTO Genres_Books (isbn, genre_id) VALUES (%s,%s)'
            values = (isbn, genre_id)
            print("Values to be inserted to Genres_Books are: ", values)
            cursor.execute(query, values)
            connection.commit() # NOTE: entry will not be inserted w/o this
            cursor.close()
            connection.close()

        return ('Book added!');

@app.route('/authors')
def authors():
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('authors.html', authors=result)

@app.route('/author/<string:author_id>/')
def author(author_id):
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn where auth.author_id = " + author_id
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('author.html', author=result)

@app.route('/add_author', methods=['POST','GET'])
def add_author():
    if request.method == 'GET':
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_author.html', books=result)

    elif request.method == 'POST':
        # Operation 1: Query to get max PK value of author_id
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT MAX(Authors.author_id) FROM Authors"
        cursor.execute(query)
        result = cursor.fetchall()
        author_id = result[0]['MAX(Authors.author_id)']
        author_id += 1
        cursor.close()
        connection.close()

        # Operation 2: Fetch Author information from form
        author_name = request.form['author_name']
        author_description = request.form['author_description']
        isbn = request.form['author_book']

        # Operation 3: Insert new Authors entry
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Authors (author_id, author_name, author_description) VALUES (%s,%s,%s)'
        values = (author_id, author_name, author_description)
        print("Values to be inserted are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        # Operation 4: Insert Books_Authors entry to link new Author to Book
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
        values = (isbn, author_id)
        print("Values to be inserted are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        return ('Author added!'); # NOTE: :( not a pretty page that displays, needs to redisplay regular website

@app.route('/genres')
def genres():
    # query 1: get genre data for list
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # query 2: get books data to list books in each genre category
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, gb.genre_id FROM Books book JOIN Genres_Books gb ON gb.isbn = book.isbn"
    cursor.execute(select_stmt)
    BooksSQL = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genres.html', genres=GenresSQL, books=BooksSQL)

# NOTE!!! Bug with this routing logic: it will only display genres for which there are books.
@app.route('/genre/<string:id>/')
def genre(id):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, book.isbn, book.book_title, genre.genre_name from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=result)

@app.route('/add_genre', methods=['POST','GET'])
def add_genre():
    if request.method == 'GET':
        return render_template('add_genre.html')

    elif request.method == 'POST':
        # query 1: get max PK value of genre_id
        # NOTE: idk if there is a way to actually do "auto increment" or if we have to do it this way??
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT MAX(Genres.genre_id) FROM Genres"
        cursor.execute(query)
        result = cursor.fetchall()
        genre_id = result[0]['MAX(Genres.genre_id)']
        genre_id += 1
        cursor.close()
        connection.close()

        # query 2: insert new value to Genres
        # NOTE: this function doesn't check to make sure a genre with same name isn't already in database!!
        genre_name = request.form['genre_name']
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Genres (genre_id, genre_name) VALUES (%s,%s)'
        values = (genre_id, genre_name)
        print("Values to be inserted are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()
        return ('Genre added!'); # NOTE: :( not a pretty page that displays, needs to redisplay regular website

@app.route('/rem_genre/<string:id>/', methods=['POST'])
# NOTE: I'm absolutely unsure what happens when you try to delete a genre that still has books associated with it
def rem_genre(id):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM Genres WHERE Genres.genre_id = " + id
    cursor.execute(query)
    connection.commit() # NOTE: entry will not be removed w/o this
    cursor.close()
    connection.close()
    return ('Genre removed!'); # NOTE: :( not a pretty page, needs to redisplay regular website

@app.route('/add_review', methods=['POST','GET'])
def add_review():
    if request.method == 'GET':
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_review.html', books=result)

    elif request.method == 'POST':
        # Step 1: Need new rating_id PK
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT MAX(Ratings.rating_id) FROM Ratings"
        cursor.execute(query)
        result = cursor.fetchall()
        rating_id = result[0]['MAX(Ratings.rating_id)']
        rating_id += 1
        cursor.close()
        connection.close()

        # Step 2: Fetch form info for Rating
        isbn = request.form['author_book']
        star_rating = request.form['user_rating']
        rating_date = time.strftime('%Y-%m-%d')

        # Step 3: Insert Rating
        # Note: review_id is initially disregarded as a foreign key to avoid insert errors, will be added in after the fact if needed. No need to initialize to NULL or anything, it will be assumed if no value is provided, it is automatically NULL.
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Ratings (rating_id, isbn, star_rating, rating_date) VALUES (%s,%s,%s,%s)'
        values = (rating_id, isbn, star_rating, rating_date)
        print("Values to be inserted into Ratings are: ", values)
        cursor.execute(query, values)
        connection.commit() # Note: if you comment this out, the Rating will not actually be added to the database, which will cause errors in all subsequent insertions/updates for this function
        cursor.close()
        connection.close()

        # Step 4: If Review not empty...
        if request.form['user_review'] != '':
            # 4a. First, need a new review_id PK for our new Review entry
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT MAX(Reviews.review_id) FROM Reviews"
            cursor.execute(query)
            result = cursor.fetchall()
            review_id = result[0]['MAX(Reviews.review_id)']
            review_id += 1
            cursor.close()
            connection.close()

            # 4b. Second, fetch Review info from form and system
            review_content = request.form['user_review']
            review_date = time.strftime('%Y-%m-%d')

            # 4c. Connect to database and add Review
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = 'INSERT INTO Reviews (review_id, rating_id, isbn, review_content, review_date) VALUES (%s,%s,%s,%s,%s)'
            values = (review_id, rating_id, isbn, review_content, review_date)
            print("Values to be inserted into Reviews are: ", values)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            # 4d. Last, update the Rating we inserted above with FK review_id
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = 'UPDATE Ratings set review_id = %s WHERE rating_id = %s'
            values = (review_id, rating_id)
            print("Values to be updated into Ratings are: ", values)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
        return ('Thank you for your rating/review!');

@app.route('/search')
def search():
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('search.html', genres=GenresSQL)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
