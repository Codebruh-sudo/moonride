#  this is the database.py

from flask_sqlalchemy import SQLAlchemy

# This creates a global SQLAlchemy object which we'll use in the app and models
db = SQLAlchemy()
