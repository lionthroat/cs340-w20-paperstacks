from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'v20501r4dkswmm9y'
app.config['MYSQL_DATABASE_PASSWORD'] = 'v19vkdjs1jevzt1b'
app.config['MYSQL_DATABASE_DB'] = 'wm1mxnjvtnaz3lv5'
app.config['MYSQL_DATABASE_HOST'] = 'spvunyfm598dw67v.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql.init_app(app)
