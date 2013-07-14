import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users

class Recipe(db.Model):
    """Models a Recipe with an author, title, avatar, and date."""
    author = db.UserProperty()
    title = db.StringProperty()
    avatar = db.BlobProperty()
    description = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
