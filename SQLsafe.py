from app import app
from flaskext.mysql import MySQL
from db import mysql
import pymysql
import pymysql.cursors

# Doesn't take parameters, returns a string or dictionary
def fetch(query = None):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    connection.commit() # equivalent of saving database changes
    dictionary = cursor.fetchall()
    cursor.close()
    connection.close()
    return dictionary

# Must have parameters, executes a db change, returns nothing
def db_query(query = None, params = ()):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    connection.commit() # equivalent of saving database changes
    cursor.close()
    connection.close()
    return

def stringsafe(string):
    quotes = "\""
    escaped_quotes = "\\\""
    quote = "\'"
    escaped_quote = "\\\'"
    string = string.replace(quotes, escaped_quotes)
    string = string.replace(quote, escaped_quote)
    return string
