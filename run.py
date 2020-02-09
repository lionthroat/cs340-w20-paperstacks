from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()

# from flask import request, redirect
# # from db_connector.db_connector import connect_to_database, execute_query
#
# # Pseudo-database for now
# # from sample_book_data.bookData import Books
# # from sample_book_data.genreData import Genres
# # # Save the return value of Books and Genres to new lists variables
# # Books = Books()
# # Genres = Genres()
#
# if __name__ == '__main__':
#     # Bind to PORT if defined, otherwise default to 5000.
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/books')
# def books():
#     return render_template('books.html', books=Books)
#
# @app.route('/book/<string:id>/')
# def book(id):
#     return render_template('book.html', id=id, book=Books[int(id)-1]) # I did some fancy bullshit and it worked??
#
# @app.route('/genres')
# def genres():
#     return render_template('genres.html', genres=Genres, books=Books)
#
# @app.route('/genre/<string:id>/')
# def genre(id):
#     return render_template('genre.html', id=int(id), genres=Genres, books=Books)
#
# @app.route('/search')
# def search(): # view functions must have unique names or everything breaks
#     return render_template('search.html')
#
# @app.route('/privacy')
# def privacy():
#     return render_template('privacy.html')
#
# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404

# @app.route('/diagnostic')
# def fetch_diagnostic():
#     print("Fetching and rendering diagnostic")
#     db_connection = connect_to_database()
#     query = "SELECT * from diagnostic;"
#     result = execute_query(db_connection, query).fetchall();
#     print(result)
#     return render_template('diagnostic_page.html', diagnostic_message=result)

# @app.route('/browse_bsg_people')
# def browse_people():
#     print("Fetching and rendering people web page")
#     db_connection = connect_to_database()
#     query = "SELECT fname, lname, homeworld, age from bsg_people;"
#     result = execute_query(db_connection, query).fetchall();
#     print(result)
#     return render_template('people_browse.html', rows=result)

# @app.route('/add_new_people', methods=['POST','GET'])
# def add_new_people():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         query = 'SELECT planet_id, name from bsg_planets'
#         result = execute_query(db_connection, query).fetchall();
#         print(result)
#
#         return render_template('people_add_new.html', planets = result)
#     elif request.method == 'POST':
#         print("Add new people!");
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']
#
#         query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#         data = (fname, lname, age, homeworld)
#         execute_query(db_connection, query, data)
#         return ('Person added!');
#
# @app.route('/db-test')
# def test_database_connection():
#     print("Executing a sample query on the database using the credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from bsg_people;"
#     result = execute_query(db_connection, query);
#     return render_template('db_test.html', rows=result)
#
# #display update form and process any updates, using the same function
# @app.route('/update_people/<int:id>', methods=['POST','GET'])
# def update_people(id):
#     db_connection = connect_to_database()
#     #display existing data
#     if request.method == 'GET':
#         people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s' % (id)
#         people_result = execute_query(db_connection, people_query).fetchone()
#
#         if people_result == None:
#             return "No such person found!"
#
#         planets_query = 'SELECT planet_id, name from bsg_planets'
#         planets_results = execute_query(db_connection, planets_query).fetchall();
#
#         return render_template('people_update.html', planets = planets_results, person = people_result)
#     elif request.method == 'POST':
#         print("Update people!");
#         character_id = request.form['character_id']
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']
#
#         print(request.form);
#
#         query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
#         data = (fname, lname, age, homeworld, character_id)
#         result = execute_query(db_connection, query, data)
#         print(str(result.rowcount) + " row(s) updated");
#
#         return redirect('/browse_bsg_people')
#
# @app.route('/delete_people/<int:id>')
# def delete_people(id):
#     '''deletes a person with the given id'''
#     db_connection = connect_to_database()
#     query = "DELETE FROM bsg_people WHERE character_id = %s"
#     data = (id,)
#
#     result = execute_query(db_connection, query, data)
#     return (str(result.rowcount) + "row deleted")
