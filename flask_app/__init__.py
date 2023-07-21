from flask import Flask
from flask_bcrypt import Bcrypt
#app = instance of Flask(class)
app = Flask(__name__)
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument
app.secret_key = "\/1rtu41-p14n0"
DATABASE = "music_db"