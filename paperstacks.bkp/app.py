import os
from flask import Flask, render_template

# from data.py, import the return value of the Tomes function
from data import Tomes

app = Flask(__name__)

# Save the return value of Tomes to a new variable
Tomes = Tomes()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/book')
# def tome():
#     return render_template('book.html')

@app.route('/tomes')
def tomes():
    return render_template('tomes.html', tomes = Tomes)

# testing purposes only
@app.route('/tome/<string:id>/')
def tome(id):
    return render_template('tome.html', id=id)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
