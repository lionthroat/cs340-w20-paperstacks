import time
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

    return render_template('home.html', genres_list=GenresSQL, featuredbooks=featuredBookSQL)

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
    # Step 1: Fetch Book's information
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
	cursor.execute(select_stmt)
	BookSQL = cursor.fetchall()
	cursor.close()
	connection.close()

    # Step 2: Fetch Book's Reviews with Ratings
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
	cursor.execute(select_stmt)
	ReviewSQL = cursor.fetchall()
	cursor.close()
	connection.close()

    # Step 3: Fetch Book's Ratings that have no Review (star rating only)
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
	cursor.execute(select_stmt)
	RatingSQL = cursor.fetchall()
	cursor.close()
	connection.close()

	return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL)

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
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        # Operation 4: Insert Books_Authors entry to link new Author to Book
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
        values = (isbn, author_id)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        url = ("/authors/" + str(author_id) + "/add_success/" + author_name + "/")
        return redirect(url)

# ADDED AUTHOR SUCCESSFULLY
@app.route('/authors/<string:author_id>/add_success/<string:author_name>/')
def successfully_added_author(author_id, author_name):
    id = int(author_id)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('authors.html', authors=result, new_author=id, new_author_name=author_name)

# EDIT AN AUTHOR
@app.route('/edit_author/<string:author_id>/', methods=['POST'])
def edit_author(author_id):
    # Get modal form information
    name = request.form['update_author_name']
    bio = request.form['update_author_bio']

    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Make sure quotes are escaped properly
    quotes = "\""
    escaped_quotes = "\\\""
    quote = "\'"
    escaped_quote = "\\\'"
    bio = bio.replace(quotes, escaped_quotes)
    bio = bio.replace(quote, escaped_quote)

    name_string = ("'" + name + "'")
    query1 = "UPDATE Authors SET author_name = " + name_string + " WHERE author_id = " + author_id

    bio_string = ("'" + bio + "'")
    query2 = "UPDATE Authors SET author_description = " + bio_string + " WHERE author_id = " + author_id

    cursor.execute(query1)
    cursor.execute(query2)

    connection.commit()
    cursor.close()
    connection.close()

    url = ("/author/" + author_id + "/edit_success/")
    return redirect(url)

# SUCCESSFULLY EDITED AN AUTHOR (redisplay author page)
@app.route('/author/<string:author_id>/edit_success/')
def successfully_edited_author(author_id):
    edit_success = 1
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn where auth.author_id = " + author_id
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('author.html', author=result, edit_success=edit_success)

# REMOVE AN AUTHOR
@app.route('/rem_author', methods=['POST'])
def rem_author():
    author_id = request.form['author_id'] # Step 1: Get Author info
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query1 = "DELETE FROM Books_Authors WHERE Books_Authors.author_id = " + author_id
    query2 = "DELETE FROM Authors WHERE Authors.author_id = " + author_id
    cursor.execute(query1)  # Step 2: Remove Author from Authors
    cursor.execute(query2)  # Step 3: Unlink Author from Books in database

    connection.commit()
    cursor.close()
    connection.close()

    url = ("/authors/rem_success")
    return redirect(url)

# REMOVED AUTHOR SUCCESSFULLY
@app.route('/authors/rem_success')
def successfully_deleted_author():
    rem_success = 1
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('authors.html', authors=result, rem_success=rem_success)

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

@app.route('/genre/<string:id>/')
def genre(id):
    # This first query returns only the genre name.
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    cursor.execute(select_stmt)
    genre_name= cursor.fetchall()
    cursor.close()
    connection.close()

    # Second query finds any books in that genre
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    books_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=genre_name, books=books_result)

# If cannot remove genre
@app.route('/genre/<string:id>/<string:error>/')
def cannot_remove_genre(id, error):
    # This first query returns only the genre name.
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    cursor.execute(select_stmt)
    genre_name= cursor.fetchall()
    cursor.close()
    connection.close()

    # Second query finds any books in that genre
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    books_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=genre_name, books=books_result, error=error)

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
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        return ('Genre added!'); # NOTE: :( not a pretty page that displays, needs to redisplay regular website

@app.route('/rem_genre/<string:id>/', methods=['POST'])
def rem_genre(id):

    # Before removing a Genre, check to make sure no Books associated with it
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "SELECT COUNT(genre.genre_id) AS `count` FROM Genres genre JOIN Genres_Books gb ON gb.genre_id = genre.genre_id JOIN Books book ON gb.isbn = book.isbn WHERE genre.genre_id = " + id
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()

    # if there ARE books still in the genre
    if result[0]['count'] != 0:
        url = ("/genre/" + id + "/" + "error/")
        print(url)
        return redirect(url)

    # Delete Genre
    else:
        # get the name of the Genre we're removing
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select genre.genre_name from Genres genre where genre.genre_id = " + id
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        genre_to_remove = result[0]['genre_name']
        cursor.close()
        connection.close()

        # delete the Genre
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "DELETE FROM Genres WHERE Genres.genre_id = " + id
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        # tell the user which Genre they have successfully removed,
        # and take them back to the main Genres page
        url = ("/genres/rem_success/" + genre_to_remove + "/")
        return redirect(url)

@app.route('/genres/rem_success/<string:genre_name>/')
def successfully_deleted_genre(genre_name):
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
    return render_template('genres.html', genres=GenresSQL, books=BooksSQL, rem_success=genre_name)

@app.route('/edit_genre/<string:genre_id>/', methods=['POST'])
def edit_genre(genre_id):
    new_name = request.form['update_genre_name']
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    name_string = ("'" + new_name + "'")
    query = "UPDATE Genres SET genre_name = " + name_string + " WHERE genre_id = " + genre_id
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    url = ("/genre/" + genre_id + "/edit_success/" + new_name + "/")
    print(url)
    return redirect(url)

# Successfully updated Genre name
@app.route('/genre/<string:id>/edit_success/<string:new_name>/')
def edit_genre_success(id, new_name):
    # This first query returns only the genre name.
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    cursor.execute(select_stmt)
    genre_name= cursor.fetchall()
    cursor.close()
    connection.close()

    # Second query finds any books in that genre
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    books_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=genre_name, books=books_result, new_name=new_name)

# REMOVE A RATING
@app.route('/rem_rating/<string:isbn>/<string:rating_id>/', methods=['POST'])
def rem_rating(isbn, rating_id):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM Ratings WHERE Ratings.rating_id = " + rating_id
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    url = ("/book/" + isbn + "/rem_rating_success/")
    return redirect(url)

# RATING REMOVED SUCCESSFULLY, REDISPLAY BOOK PAGE
@app.route('/book/<string:isbn>/rem_rating_success/')
def rating_removed_successfully(isbn):
    rating_rem = "The rating removal succeeded"
    # Step 1: Fetch Book's information
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    cursor.execute(select_stmt)
    BookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 2: Fetch Book's Reviews with Ratings
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    cursor.execute(select_stmt)
    ReviewSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 3: Fetch Book's Ratings that have no Review (star rating only)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    cursor.execute(select_stmt)
    RatingSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, rating_rem=rating_rem)

# REMOVE A RATING
@app.route('/rem_review/<string:isbn>/<string:review_id>/', methods=['POST'])
def rem_review(isbn, review_id):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM Reviews WHERE Reviews.review_id = " + review_id
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    url = ("/book/" + isbn + "/rem_review_success/")
    return redirect(url)

# REVIEW REMOVED SUCCESSFULLY, REDISPLAY BOOK PAGE
@app.route('/book/<string:isbn>/rem_review_success/')
def review_removed_successfully(isbn):
    review_rem = "The review removal succeeded"
    # Step 1: Fetch Book's information
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    cursor.execute(select_stmt)
    BookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 2: Fetch Book's Reviews with Ratings
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    cursor.execute(select_stmt)
    ReviewSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 3: Fetch Book's Ratings that have no Review (star rating only)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    cursor.execute(select_stmt)
    RatingSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, review_rem=review_rem)

# EDIT REVIEW CONTENT
@app.route('/edit_review/<string:isbn>/<string:review_id>/', methods=['POST'])
def edit_review(isbn, review_id):
    content = request.form['update_review_content']
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    content_string = ("'" + content + "'")
    query = "UPDATE Reviews SET review_content = " + content_string + " WHERE review_id = " + review_id
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    url = ("/book/" + isbn + "/rem_review_success/")
    return redirect(url)

# REVIEW WAS EDITED SUCCESSFULLY
@app.route('/book/<string:isbn>/edit_rev_success/')
def review_edit_successfully(isbn):
    review_edit = "The review edit succeeded"
    # Step 1: Fetch Book's information
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    cursor.execute(select_stmt)
    BookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 2: Fetch Book's Reviews with Ratings
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    cursor.execute(select_stmt)
    ReviewSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 3: Fetch Book's Ratings that have no Review (star rating only)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    cursor.execute(select_stmt)
    RatingSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, review_edit=review_edit)

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
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            # 4d. Last, update the Rating we inserted above with FK review_id
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = 'UPDATE Ratings set review_id = %s WHERE rating_id = %s'
            values = (review_id, rating_id)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

        url = ("/book/" + isbn + "/add_rev_success/")
        return redirect(url)

# NEW REVIEW WAS ADDED SUCCESSFULLY
@app.route('/book/<string:isbn>/add_rev_success/')
def review_add_success(isbn):
    review_add = "The review add succeeded"
    # Step 1: Fetch Book's information
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    cursor.execute(select_stmt)
    BookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 2: Fetch Book's Reviews with Ratings
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    cursor.execute(select_stmt)
    ReviewSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 3: Fetch Book's Ratings that have no Review (star rating only)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    cursor.execute(select_stmt)
    RatingSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, review_add=review_add)

# EDIT STAR RATING
@app.route('/edit_rating/<string:isbn>/<string:rating_id>/', methods=['POST'])
def edit_rating(isbn, rating_id):
    star_rating = request.form['update_rating']
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "UPDATE Ratings SET star_rating = " + star_rating + " WHERE rating_id = " + rating_id
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    url = ("/book/" + isbn + "/edit_rating_success/")
    return redirect(url)

# RATING WAS EDITED SUCCESSFULLY
@app.route('/book/<string:isbn>/edit_rating_success/')
def rating_edit_successfully(isbn):
    rating_edit = "The rating edit succeeded"
    # Step 1: Fetch Book's information
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    cursor.execute(select_stmt)
    BookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 2: Fetch Book's Reviews with Ratings
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    cursor.execute(select_stmt)
    ReviewSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # Step 3: Fetch Book's Ratings that have no Review (star rating only)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    cursor.execute(select_stmt)
    RatingSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, rating_edit=rating_edit)

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'GET':
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
        cursor.execute(select_stmt)
        GenresSQL = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('search.html', genres_list=GenresSQL)

    elif request.method == 'POST':

        # NAVBAR SEARCH
        if request.form['search_submit'] == 'navbar_search':
            search_query = request.form['tiny']

            # retrieve genre data from database for search form
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
            cursor.execute(select_stmt)
            GenresSQL = cursor.fetchall()
            cursor.close()
            connection.close()

            # search 1: look for search term in Books
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            search_string = ("'%" + search_query + "%'") # allows substring search from book titles
            select_stmt = "SELECT book.isbn, book.book_title FROM Books book WHERE book.book_title LIKE" + search_string # put together final query
            cursor.execute(select_stmt)
            books = cursor.fetchall()
            cursor.close()
            connection.close()

            # search 2: look for search term in Authors
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            search_string = ("'%" + search_query + "%'") # allows substring search from author names
            select_stmt = "SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE " + search_string # put together final query
            cursor.execute(select_stmt)
            authors = cursor.fetchall()
            cursor.close()
            connection.close()

            # search 3: look for search term in Genres
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            search_string = ("'%" + search_query + "%'") # allows substring search from genres names
            select_stmt = "SELECT genre.genre_id, genre.genre_name FROM Genres genre WHERE genre.genre_name LIKE " + search_string # put together final query
            cursor.execute(select_stmt)
            genres = cursor.fetchall()
            cursor.close()
            connection.close()

            return render_template('search.html', search_query=search_query, genres_list=GenresSQL, books=books, authors=authors, genres=genres)

        # ADVANCED SEARCH
        elif request.form['search_submit'] == 'advanced_search':
            # fetch form data from advanced search on /search
            title = request.form['search_title']
            author = request.form['search_author']
            year = request.form['search_year']
            isbn = request.form['search_isbn']
            genre = request.form['search_genre']

            # advanced search operation 1: look for search term(s) in Books
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            search_string = ("'%" + title + "%'") # allows substring search from book titles
            select_stmt = "SELECT book.isbn, book.book_title, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id WHERE " # put together final query

            query_num = 0
            if title != '':
                title_select = "book.book_title LIKE " + ("'%" + title + "%'")
                search_query = "Title: " + title

                select_stmt = select_stmt + title_select
                query_num += 1

            if year != '':
                if query_num != 0:
                    year_select = " AND book.year_published = " + year
                    search_query = search_query + ", Year Published: " + year
                else:
                    year_select = "book.year_published = " + year
                    search_query = "Year Published: " + year

                select_stmt = select_stmt + year_select
                query_num += 1

            if isbn != '':
                if query_num != 0:
                    isbn_select = " AND book.isbn = " + isbn
                    search_query = search_query + ", ISBN-10: " + isbn
                else:
                    isbn_select = "book.isbn = " + isbn
                    search_query = "ISBN-10: " + isbn

                select_stmt = select_stmt + isbn_select
                query_num += 1

            if author != '':
                if query_num != 0:
                    author_select = " AND auth.author_name LIKE " + ("'%" + author + "%'")
                    search_query = search_query + ", Author: " + author
                else:
                    author_select = "auth.author_name LIKE " + ("'%" + author + "%'")
                    search_query = "Author: " + author

                select_stmt = select_stmt + author_select
                query_num += 1

            if genre != '':
                if query_num != 0:
                    genre_select = " AND genre.genre_id = " + genre
                    search_query = search_query + ", Genre: " + genre
                else:
                    genre_select = "genre.genre_id = " + genre
                    search_query = "Genre: " + genre

                select_stmt = select_stmt + genre_select
                query_num += 1

            select_stmt = select_stmt + " GROUP BY book.isbn ORDER BY book.book_title ASC"
            cursor.execute(select_stmt)
            books = cursor.fetchall()
            cursor.close()
            connection.close()

            # advanced search operation 2: look for search term(s) in Authors
            if author != '':
                connection = mysql.connect()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                search_string = ("'%" + author + "%'") # allows substring search from author names
                select_stmt = "SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE " + search_string # put together final query
                cursor.execute(select_stmt)
                authorResult = cursor.fetchall()
                cursor.close()
                connection.close()
            else:
                authorResult = ''

            # Page display: retrieve genre data from database for search form
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
            cursor.execute(select_stmt)
            GenresSQL = cursor.fetchall()
            cursor.close()
            connection.close()

            return render_template('search.html', search_query=search_query, genres_list=GenresSQL, books=books, authors=authorResult)


        # search (user pressed search but didn't enter query)
        else:
            # retrieve genre data from database for search form
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
