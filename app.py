# Flask app
# @heatherdiruscio, 1/7/2019
# Based on tutorial at:
# https://www.youtube.com/watch?v=zRwy8gtgJ1A


# note: this app.py file is the equivalent
# of server.js in Node.js

from flask import Flask, render_template

# from data.py, import the return value of the Articles function
from data import Articles

app = Flask(__name__)

# Save the return value of Articles to a new variable
Articles = Articles()

# first route for homepage
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

# as long as app.run() is given the argument debug=True,
# we don't have to quit and restart server from terminal
# every time we make an update and want to see updated page
# in our web browser. It can be removed and the program
# still works, but more restarts may be necessary
if __name__ == '__main__':
    app.run(debug=True)
