import time
from app import app
from SQLsafe import fetch, db_query, stringsafe
from flask import Flask, Response, render_template
from flask import request, redirect

from code_msgs import Messages
Messages = Messages()

from flaskext.mysql import MySQL
from db import mysql
import pymysql
import pymysql.cursors

@app.route('/')
def index():
    select = "select genre.genre_id, genre.genre_name from Genres genre order by genre.genre_name"
    GenresSQL = fetch(select) # query 1: get genres for left sidebar links

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id WHERE book.book_title = 'Electric Arches';"
    featuredBookSQL = fetch(select) # query 2: get featured book data

    return render_template('home.html', genres_list=GenresSQL, featuredbooks=featuredBookSQL)

@app.route('/books')
def books():
    select = "SELECT Books.isbn, Books.book_title FROM Books WHERE NOT EXISTS(SELECT isbn FROM Books_Authors WHERE Books_Authors.isbn=Books.isbn)"
    orphans = fetch(select) # Get all Books without Authors and put them in their own dictionary, otherwise they won't display

    select = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id order by book.book_title ASC"
    books = fetch(select)

    return render_template('books.html', books=books, orphans=orphans)

@app.route('/books/<string:code>')
def books_update(code):
    code = int(code)
    code_msg = Messages[code]

    select = "SELECT Books.isbn, Books.book_title FROM Books WHERE NOT EXISTS(SELECT isbn FROM Books_Authors WHERE Books_Authors.isbn=Books.isbn)"
    orphans = fetch(select) # Get all Books without Authors and put them in their own dictionary, otherwise they won't display

    select = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id order by book.book_title ASC"
    books = fetch(select)

    return render_template('books.html', books=books, orphans=orphans, code=code, code_msg=code_msg)

@app.route('/book/<string:isbn>/')
def book(isbn):
    # Step 1: Fetch Book's information (Returns 1 entry per genre for the book - this is fine!)
    select = "SELECT book.isbn, book.book_title, book.year_published, book.book_description, genre.genre_name from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    book = fetch(select)

    # Step 2: Fetch Book's Author(s) - may be none
    select = "SELECT auth.author_name, auth.author_id from Authors auth JOIN Books_Authors ba ON ba.author_id = auth.author_id where ba.isbn = " + isbn
    authors = fetch(select)

    # Step 3: Get Avg Rating (float avg, total # of ratings)
    select = "SELECT AVG(star_rating) AS `average_rating`, COUNT(rate.rating_id) AS `rating_count` FROM Ratings rate WHERE rate.isbn = " + isbn
    AvgRatingSQL = fetch(select)

    # Initialize so that book.html doesn't break expecting these vars
    float_avg = None
    int_avg = None
    rating_count = None

    if AvgRatingSQL[0]['rating_count'] != 0:
        float_avg = round(AvgRatingSQL[0]['average_rating'], 2)
        int_avg = round(AvgRatingSQL[0]['average_rating'])
        rating_count = AvgRatingSQL[0]['rating_count']

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 4: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 5: Fetch Book's Ratings that have no Review

    # Step 6: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    all_genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    all_authors = fetch(select)

    return render_template('book.html', book=book, authors=authors, reviews=ReviewSQL, ratings=RatingSQL, all_genres=all_genres, all_authors=all_authors, rating_count=rating_count, int_avg=int_avg, float_avg=float_avg)

# Something was changed, redisplay book page and give user message
@app.route('/book/<string:isbn>/update/<string:code>')
def book_updated(isbn, code):
    code = int(code)
    code_msg = Messages[code]

    # Step 1: Fetch Book's information (Returns 1 entry per genre for the book - this is fine!)
    select = "SELECT book.isbn, book.book_title, book.year_published, book.book_description, genre.genre_name from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    book = fetch(select)

    # Step 2: Fetch Book's Author(s) - may be none
    select = "SELECT auth.author_name, auth.author_id from Authors auth JOIN Books_Authors ba ON ba.author_id = auth.author_id where ba.isbn = " + isbn
    authors = fetch(select)

    # Step 3: Get Avg Rating (float avg, total # of ratings)
    select = "SELECT AVG(star_rating) AS `average_rating`, COUNT(rate.rating_id) AS `rating_count` FROM Ratings rate WHERE rate.isbn = " + isbn
    AvgRatingSQL = fetch(select)

    # Initialize so that book.html doesn't break expecting these vars
    float_avg = None
    int_avg = None
    rating_count = None

    if AvgRatingSQL[0]['rating_count'] != 0:
        float_avg = round(AvgRatingSQL[0]['average_rating'], 2)
        int_avg = round(AvgRatingSQL[0]['average_rating'])
        rating_count = AvgRatingSQL[0]['rating_count']

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 4: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 5: Fetch Book's Ratings that have no Review

    # Step 6: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    all_genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    all_authors = fetch(select)

    return render_template('book.html', book=book, authors=authors, reviews=ReviewSQL, ratings=RatingSQL, all_genres=all_genres, all_authors=all_authors, rating_count=rating_count, int_avg=int_avg, float_avg=float_avg, code_msg=code_msg, code=code)

@app.route('/add_book', methods=['POST','GET'])
def add_book():
    if request.method == 'GET':
        select = "select genre.genre_id, genre.genre_name from Genres genre;"
        GenresSQL = fetch(select) # Get Genres information

        select = "select auth.author_id, auth.author_name from Authors auth;"
        AuthorsSQL = fetch(select) # Get Current Authors information

        return render_template('add_book.html', genres=GenresSQL, authors=AuthorsSQL)

    elif request.method == 'POST':
        code = "0" # Status code set to default
        # Operation 1: Fetch Book information from form
        book_title = request.form['book_title']
        isbn = request.form['book_isbn']
        year_published = int(request.form['book_year'])
        book_description = request.form['book_description']
        book_description = stringsafe(book_description)

        # Insert New Book
        query = 'INSERT INTO Books (isbn, book_title, year_published, book_description) VALUES (%s, %s, %s, %s)'
        values = (isbn, book_title, year_published, book_description)
        db_query(query, values)

        # Associate Book with one or more Genres, via Genres_Books entries
        genre_ids = request.form.getlist('book_genre') # use getlist to get data from select multiple
        genre_ids = list(map(int, genre_ids)) # list comprehension: turn into ints that can be inserted
        # results = list(map(int, results))  # functional programming solution: map list to ints
        # results = [int(i) for i in results] # more pythonic solution: list comprehension
        for genre in genre_ids:
            query = 'INSERT INTO Genres_Books (isbn, genre_id) VALUES (%s, %s)'
            values = (isbn, genre)
            db_query(query, values)

        # Chose Existing Author(s), add Books_Authors entries
        if len(request.form.getlist('book_author')) != 0:
            author_ids = request.form.getlist('book_author') # use getlist for select multiple
            author_ids = list(map(int, author_ids)) # list comprehension: turn into ints that can be inserted

            for author in author_ids:
                query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s, %s)'
                values = (isbn, author)
                db_query(query, values)

        # Chose New Author, add Author then add Books_Authors entries
        elif len(request.form['author_name']) != 0 and len(request.form['author_description']) != 0:
            author_name = request.form['author_name']
            author_name = stringsafe(author_name)
            author_description = request.form['author_description']
            author_description = stringsafe(author_name)

            select = "SELECT MAX(Authors.author_id) FROM Authors"
            result = fetch(select)
            author_id = result[0]['MAX(Authors.author_id)']
            author_id += 1

            query = 'INSERT INTO Authors (author_id, author_name, author_description) VALUES (%s,%s,%s)'
            values = (author_id, author_name, author_description)
            db_query(query, values)

            query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
            values = (isbn, author_id)
            db_query(query, values)

            code = "32" # Successfully added book AND author

        # Did not enter Authors, can do later
        else:
            print("no author")
            code = "31" # Book added but without authors

        if code == "0":
            code = "3" # If nothing went wrong, assume success. 3 is add book success code

        isbn = str(isbn)
        url = ("/book/" + isbn + "/update/" + code)
        return redirect(url)

@app.route('/edit_book/<string:isbn>/', methods=['POST'])
def edit_book(isbn):
    code = "0"

    # Update Book Title
    if request.form['update_title'] != '':
        title = request.form['update_title']
        title = stringsafe(title)
        query = "UPDATE Books SET book_title = %s WHERE isbn = %s"
        values = (title, isbn)
        db_query(query, values)

    # Update Book Description
    if request.form['update_book_description'] != '':
        description = request.form['update_book_description']
        description = stringsafe(description)  # add escape characters to single and double quotes
        query = "UPDATE Books SET book_description = %s WHERE isbn = %s"
        values = (description, isbn) # this automatically adds '' around strings. do not add manually
        db_query(query, values)

    # Update Year Published
    if request.form['update_year'] != '':
        year = request.form['update_year']
        if (int(year) >= 0) and (int(year) < 2025):
            query = "UPDATE Books SET year_published = %s WHERE isbn = %s"
            values = (year, isbn)
            db_query(query, values)
        else:
            code = "2"

    # Update Author(s)
    if len(request.form.getlist('update_author')) != 0:
        # Delete all previous Books_Authors entries first, so there are no orphans
        query = "DELETE FROM Books_Authors WHERE Books_Authors.isbn = %s"
        values = (isbn)
        db_query(query, values)

        # Then get our new list
        authors = request.form.getlist('update_author')
        for author_id in authors:
            query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
            values = (isbn, author_id)
            db_query(query, values) # Insert one or more Books_Authors entries

    # Update Genre(s)
    if len(request.form.getlist('update_genre')) != 0:
        # Delete all previous Genres_Books entries first, so there are no orphans
        query = "DELETE FROM Genres_Books WHERE Genres_Books.isbn = %s"
        values = (isbn)
        db_query(query, values)

        # Then get our new list
        genres = request.form.getlist('update_genre')
        for genre_id in genres:
            query = 'INSERT INTO Genres_Books (isbn, genre_id) VALUES (%s,%s)'
            values = (isbn, genre_id)
            db_query(query, values) # Insert one or more Genres_Books entries

    if code != "2": # If no known issues with book edit
        code = "1" # Report book edit success

    url = ("/book/" + isbn + "/update/" + code)
    return redirect(url)

# Delete a book
@app.route('/rem_book/<string:isbn>/', methods=['POST'])
def rem_book(isbn):

    # Before removing a Book, check to make sure no Authors would be left without at least one Book

    # Step 1: Get the list of authors for this book
    select = "SELECT ba.author_id from Books_Authors ba where ba.isbn = " + isbn
    author_ids = fetch(select)

    # Step 2: For all authors listed on this book, see how many books they have in the database. If any of them only have 1 book counted, that means they would be left without books if this one were removed, so the removal needs to be aborted and the user notified of the reason.
    for author in author_ids:
        auth = str(author['author_id'])
        select = "SELECT COUNT(ba.isbn) AS `book_count` FROM Books_Authors ba WHERE ba.author_id = " + auth
        result = fetch(select)
        # If author only has one book, abort and redirect
        if result[0]['book_count'] == 1:
            code = "6"
            url = ("/book/" + isbn + "/update/" + code)
            return redirect(url)

    # Step 3: If there were no issues with orphaned authors, delete all Books_Authors entries for this book
    query = "DELETE FROM Books_Authors WHERE Books_Authors.isbn = %s"
    values = (isbn)
    db_query(query, values)

    query = "DELETE FROM Genres_Books WHERE Genres_Books.isbn = %s"
    values = (isbn)
    db_query(query, values)

    # Step 4: Finally, delete the Book
    query = "DELETE FROM Books WHERE Books.isbn = %s"
    values = (isbn)
    db_query(query, values)

    code = "5" # Report book delete success
    url = ("/books/" + code)
    return redirect(url)

# See a list of all authors
@app.route('/authors')
def authors():
	select = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
	result = fetch(select)
	return render_template('authors.html', authors=result)

# See one author
@app.route('/author/<string:author_id>/')
def author(author_id):
    select = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn where auth.author_id = " + author_id
    author = fetch(select)
    return render_template('author.html', author=author)

# Add a new author
@app.route('/add_author', methods=['POST','GET'])
def add_author():
    if request.method == 'GET':
        select = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        result = fetch(select)
        return render_template('add_author.html', books=result)

    elif request.method == 'POST':
        select = "SELECT MAX(Authors.author_id) FROM Authors"
        result = fetch(select) # Step 1: Query to get max PK value of author_id
        author_id = result[0]['MAX(Authors.author_id)']
        author_id += 1

        # Step 2: Fetch Author information from form
        author_name = request.form['author_name']
        author_description = request.form['author_description']
        isbn = request.form['author_book']

        query = 'INSERT INTO Authors (author_id, author_name, author_description) VALUES (%s,%s,%s)'
        values = (author_id, author_name, author_description)
        db_query(query, values) # Step 3: Insert new Authors entry

        query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
        values = (isbn, author_id)
        db_query(query, values) # Step 4: Insert Books_Authors entry to link new Author to Book

        url = ("/authors/" + str(author_id) + "/add_success/" + author_name + "/")
        return redirect(url)

# Author was added successfully
@app.route('/authors/<string:author_id>/add_success/<string:author_name>/')
def successfully_added_author(author_id, author_name):
    id = int(author_id)
    select = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn GROUP BY auth.author_id ORDER BY auth.author_name"
    result = fetch(select)
    return render_template('authors.html', authors=result, new_author=id, new_author_name=author_name)

# Edit an Author
@app.route('/edit_author/<string:author_id>/', methods=['POST'])
def edit_author(author_id):

    # Step 1: Update name
    name = request.form['update_author_name']
    name = stringsafe(name)
    query = "UPDATE Authors SET author_name = %s WHERE author_id = %s"
    values = (name, author_id)
    db_query(query, values)

    # Step 2: Update author bio
    bio = request.form['update_author_bio']
    bio = stringsafe(bio) # add escape characters to single and double quotes
    query = "UPDATE Authors SET author_description = %s WHERE author_id = %s"
    values = (bio, author_id)
    db_query(query, values)

    url = ("/author/" + author_id + "/edit_success/")
    return redirect(url)

# Author was edited successfully, redisplay author page.
@app.route('/author/<string:author_id>/edit_success/')
def successfully_edited_author(author_id):
    edit_success = 1
    select = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn where auth.author_id = " + author_id
    result = fetch(select)
    return render_template('author.html', author=result, edit_success=edit_success)

# Remove an author
@app.route('/rem_author', methods=['POST'])
def rem_author():
    author_id = request.form['author_id'] # Step 1: Get Author info

    query = "DELETE FROM Books_Authors WHERE Books_Authors.author_id = %s"
    values = (author_id)
    db_query(query, values)

    query = "DELETE FROM Authors WHERE Authors.author_id = %s"
    db_query(query, values)

    url = ("/authors/rem_success")
    return redirect(url)

# Author was removed successfully
@app.route('/authors/rem_success')
def successfully_deleted_author():
    rem_success = 1
    select = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
    result = fetch(select)
    return render_template('authors.html', authors=result, rem_success=rem_success)

@app.route('/genres')
def genres():
    select = "select genre.genre_id, genre.genre_name from Genres genre;"
    GenresSQL = fetch(select) # query 1: get genre data for list

    select = "select book.isbn, book.book_title, gb.genre_id FROM Books book JOIN Genres_Books gb ON gb.isbn = book.isbn"
    BooksSQL = fetch(select) # query 2: list books in each genre

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

# Add a new Genre
@app.route('/add_genre', methods=['POST','GET'])
def add_genre():
    if request.method == 'GET':
        return render_template('add_genre.html')

    elif request.method == 'POST':
        select = "SELECT MAX(Genres.genre_id) FROM Genres"
        result = fetch(select) # query 1: get max PK value of genre_id
        genre_id = result[0]['MAX(Genres.genre_id)']
        genre_id += 1

        genre_name = request.form['genre_name']
        query = 'INSERT INTO Genres (genre_id, genre_name) VALUES (%s,%s)'
        values = (genre_id, genre_name)
        db_query(query, values) # query 2: insert new value to Genres

        return ("Genre added! <a href='/'>(back to paperstacks)</a>");

# Remove a Genre
@app.route('/rem_genre/<string:id>/', methods=['POST'])
def rem_genre(id):

    select = "SELECT COUNT(genre.genre_id) AS `count` FROM Genres genre JOIN Genres_Books gb ON gb.genre_id = genre.genre_id JOIN Books book ON gb.isbn = book.isbn WHERE genre.genre_id = " + id
    result = fetch(select) # Step 1: Check to make sure no Books associated with this Genre

    # if there ARE books still in the genre
    if result[0]['count'] != 0:
        url = ("/genre/" + id + "/" + "error/")
        print(url)
        return redirect(url)

    # Delete Genre
    else:
        select = "select genre.genre_name from Genres genre where genre.genre_id = " + id
        result = fetch(select) # get the name of the Genre we're removing
        genre_to_remove = result[0]['genre_name']

        query = "DELETE FROM Genres WHERE Genres.genre_id = %s"
        values = (id)
        db_query(query, values) # delete the Genre

        url = ("/genres/rem_success/" + genre_to_remove + "/")
        return redirect(url)

# Genre was removed successfully
@app.route('/genres/rem_success/<string:genre_name>/')
def successfully_deleted_genre(genre_name):

    select = "select genre.genre_id, genre.genre_name from Genres genre;"
    GenresSQL = fetch(select) # query 1: get genre data for list

    select = "select book.isbn, book.book_title, gb.genre_id FROM Books book JOIN Genres_Books gb ON gb.isbn = book.isbn"
    BooksSQL = fetch(select) # query 2: books in each genre

    return render_template('genres.html', genres=GenresSQL, books=BooksSQL, rem_success=genre_name)

# Edit a Genre
@app.route('/edit_genre/<string:genre_id>/', methods=['POST'])
def edit_genre(genre_id):
    new_name = request.form['update_genre_name']
    name_string = ("'" + new_name + "'")

    query = "UPDATE Genres SET genre_name = %s WHERE genre_id = %s"
    values = (name_string, genre_id)
    db_query(query, values)

    url = ("/genre/" + genre_id + "/edit_success/" + new_name + "/")
    print(url)
    return redirect(url)

# Successfully updated Genre name
@app.route('/genre/<string:id>/edit_success/<string:new_name>/')
def edit_genre_success(id, new_name):

    select = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    genre_name = fetch(select) # returns only the genre name.

    select = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    books_result = fetch(select) # Second query finds any books in that genre

    return render_template('genre.html', genreinfo=genre_name, books=books_result, new_name=new_name)

# Remove a Rating
@app.route('/rem_rating/<string:isbn>/<string:rating_id>/', methods=['POST'])
def rem_rating(isbn, rating_id):
    query = "DELETE FROM Ratings WHERE Ratings.rating_id = %s"
    values = (rating_id)
    db_query(query, values)
    code = "23" # rating delete success code
    url = ("/book/" + isbn + "/update/" + code)
    return redirect(url)

# Remove a review
@app.route('/rem_review/<string:isbn>/<string:review_id>/', methods=['POST'])
def rem_review(isbn, review_id):

    query = "DELETE FROM Reviews WHERE Reviews.review_id = %s"
    values = (review_id)
    db_query(query, values)

    code = "17" # Review delete success code
    url = ("/book/" + isbn + "/update/" + code)
    return redirect(url)

# Edit review
@app.route('/edit_review/<string:isbn>/<string:review_id>/', methods=['POST'])
def edit_review(isbn, review_id):
    content = request.form['update_review_content']
    content_string = ("'" + content + "'")

    query = "UPDATE Reviews SET review_content = %d WHERE review_id = %s"
    values = (content_string, review_id)
    db_query(query, values)

    code = "13" # Review edit success code
    url = ("/book/" + isbn + "/update/" + code)
    return redirect(url)

# Add a new rating/review
@app.route('/add_review', methods=['POST','GET'])
def add_review():
    if request.method == 'GET':
        select = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        result = fetch(select)
        return render_template('add_review.html', books=result)

    elif request.method == 'POST':
        # Step 1: Need new rating_id PK
        select = "SELECT MAX(Ratings.rating_id) FROM Ratings"
        result = fetch(select)
        rating_id = result[0]['MAX(Ratings.rating_id)']
        rating_id += 1

        # Step 2: Fetch form info for Rating
        isbn = request.form['author_book']
        star_rating = request.form['user_rating']
        rating_date = time.strftime('%Y-%m-%d')

        # Step 3: Insert Rating, Note: review_id initially disregarded as FK to avoid insert errors
        query = 'INSERT INTO Ratings (rating_id, isbn, star_rating, rating_date) VALUES (%s,%s,%s,%s)'
        values = (rating_id, isbn, star_rating, rating_date)
        db_query(query, values)

        # Step 4: If Review not empty...
        if request.form['user_review'] != '':
            # 4a. First, need a new review_id PK for our new Review entry
            select = "SELECT MAX(Reviews.review_id) FROM Reviews"
            result = fetch(select)
            review_id = result[0]['MAX(Reviews.review_id)']
            review_id += 1

            # 4b. Second, fetch Review info from form and system
            review_content = request.form['user_review']
            review_date = time.strftime('%Y-%m-%d')

            query = 'INSERT INTO Reviews (review_id, rating_id, isbn, review_content, review_date) VALUES (%s,%s,%s,%s,%s)'
            values = (review_id, rating_id, isbn, review_content, review_date)
            db_query(query, values) # 4c. Connect to database and add Review

            # 4d. Last, update the Rating we inserted above with FK review_id
            query = 'UPDATE Ratings set review_id = %s WHERE rating_id = %s'
            values = (review_id, rating_id)
            db_query(query, values)

        code = "15" # Review/Rating add success
        url = ("/book/" + isbn + "/update/" + code)
        return redirect(url)

# Edit a rating
@app.route('/edit_rating/<string:isbn>/<string:rating_id>/', methods=['POST'])
def edit_rating(isbn, rating_id):
    star_rating = request.form['update_rating']
    query = "UPDATE Ratings SET star_rating = %s WHERE rating_id = %s"
    values = (star_rating, rating_id)
    db_query(query, values)

    code = "19" # Rating edit success code
    url = ("/book/" + isbn + "/update/" + code)
    return redirect(url)

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'GET':
        select = "select genre.genre_id, genre.genre_name from Genres genre;"
        GenresSQL = fetch(select)
        return render_template('search.html', genres_list=GenresSQL)

    elif request.method == 'POST':

        # NAVBAR SEARCH
        if request.form['search_submit'] == 'navbar_search':
            search_query = request.form['tiny']
            search_string = ("'%" + search_query + "%'") # allows substring searches

            select = "select genre.genre_id, genre.genre_name from Genres genre;"
            GenresSQL = fetch(select) # retrieve genre data from database

            select = "SELECT book.isbn, book.book_title FROM Books book WHERE book.book_title LIKE" + search_string # put together final query
            books = fetch(select) # search 1: look for search term in Books

            select = "SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE " + search_string # put together final query
            authors = fetch(select) # search 2: look for search term in Authors

            select = "SELECT genre.genre_id, genre.genre_name FROM Genres genre WHERE genre.genre_name LIKE " + search_string # put together final query
            genres = fetch(select) # search 3: look for search term in Genres

            return render_template('search.html', search_query=search_query, genres_list=GenresSQL, books=books, authors=authors, genres=genres)

        # ADVANCED SEARCH
        elif request.form['search_submit'] == 'advanced_search':
            # fetch form data from advanced search on /search
            title = request.form['search_title']
            author = request.form['search_author']
            year = request.form['search_year']
            isbn = request.form['search_isbn']
            genre = request.form['search_genre']
            rating = request.form['search_rating']
            review = request.form.get('search_has_reviews')
            query_num = 0 # count how many search criteria we have

            # If not searching by rating or reviews
            if rating == 'null' and review is None:
                # This just kicks off the search query, doesn't search for anything yet
                select_stmt = "SELECT book.isbn, book.book_title, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id WHERE "
                having_flag = 0
                # the rating_flag set to 0 tells the query it still needs to add GROUP BY at the end. If user is also searching by rating, this will already be in the query because GROUP BY breaks a query if it comes after HAVING

            # Else, if searching by BOTH ratings and reviews
            elif rating != 'null' and review == 'has_reviews':
                # Note: The SQL query is structured differently if the user wants to search by average star rating. Because this category is calculated on the fly, and is not a stored attribute of any table, setting the ad hoc column `average_rating` and then searching by it will break a query if you use WHERE (e.g. WHERE average_rating = 3). This is because SQL evaluates queries backwards, from right to left, so average_rating does not exist at the time it is being referenced. To fix this, a query involving average star ratings uses HAVING, which has deferred evaluation.
                select_stmt = "SELECT book.isbn, book.book_title, COUNT(rev.review_id) AS `num_reviews`, ROUND(AVG(rate.star_rating)) AS `average_rating`, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id JOIN Ratings rate ON rate.isbn = book.isbn JOIN Reviews rev ON rev.isbn = book.isbn GROUP BY book.isbn HAVING num_reviews > 0 AND average_rating = " + rating
                search_query = "Has Reviews, Average Rating: " + rating
                having_flag = 1
                query_num += 1

            # Else, if searching by only ratings, not reviews
            elif rating != 'null' and review is None:
                select_stmt = "SELECT book.isbn, book.book_title, ROUND(AVG(rate.star_rating)) AS `average_rating`, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id JOIN Ratings rate ON rate.isbn = book.isbn GROUP BY book.isbn HAVING average_rating = " + rating
                search_query = "Average Rating: " + rating
                having_flag = 1
                query_num += 1

            # Else, search by only whether it has reviews, not by average ratings
            else:
                select_stmt = "SELECT book.isbn, book.book_title, COUNT(rev.review_id) AS `num_reviews`, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id JOIN Reviews rev ON rev.isbn = book.isbn GROUP BY book.isbn HAVING num_reviews > 0"
                search_query = "Has Reviews"
                having_flag = 1
                query_num += 1

            if title != '': # if title search is not empty
                if query_num == 0: # and if this is the first filter we're adding
                    title_select = "book.book_title LIKE " + ("'%" + title + "%'")
                    search_query = "Title: " + title
                else: # else we added a star rating filter first
                    title_select = " AND book.book_title LIKE " + ("'%" + title + "%'")
                    search_query = search_query + ", Title: " + title

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

            if having_flag == 0:
                select_stmt = select_stmt + " GROUP BY book.isbn"

            select_stmt = select_stmt + " ORDER BY book.book_title ASC"

            print("Search SQL:", select_stmt)
            books = fetch(select_stmt)

            # advanced search operation 2: look for search term(s) in Authors
            if author != '':
                search_string = ("'%" + author + "%'") # allows substring search from author names
                select = "SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE " + search_string # put together final query
                authorResult = fetch(select)
            else:
                authorResult = ''

            select = "select genre.genre_id, genre.genre_name from Genres genre;"
            GenresSQL = fetch(select) # Page display: retrieve genre data

            return render_template('search.html', search_query=search_query, genres_list=GenresSQL, books=books, authors=authorResult)

        else: # (user pressed search but didn't enter query)
            select = "select genre.genre_id, genre.genre_name from Genres genre;"
            GenresSQL = fetch(select)
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

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()
