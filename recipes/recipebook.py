import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class Recipe(db.Model):
    """Models a Recipe with an author, content, avatar, and date."""
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    avatar = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)


def recipe_key(recipe_name=None):
    """Constructs a Datastore key for a Recipe entity with recipe_name."""
    return db.Key.from_path('Recipe', recipe_name or 'default_recipe')


class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.out.write('<html><body>')
        recipe_name=self.request.get('recipe_name')

        recipes = db.GqlQuery('SELECT * '
                                'FROM Recipe '
                                'WHERE ANCESTOR IS :1 '
                                'ORDER BY date DESC LIMIT 10',
                                recipe_key(recipe_name))
        
        template_values = {
            'recipes': recipes,
            #'url': url,
            #'url_linktext': url_linktext,
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Image(webapp2.RequestHandler):
    def get(self):
        recipe = db.get(self.request.get('img_id'))
        if recipe.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(recipe.avatar)
        else:
            self.response.out.write('No image')


class Recipebook(webapp2.RequestHandler):
    def post(self):
        recipe_name = self.request.get('recipe_name')
        recipe = Recipe(parent=recipe_key(recipe_name))

        if users.get_current_user():
            recipe.author = users.get_current_user()

        recipe.content = self.request.get('content')
        avatar = images.resize(self.request.get('img'), 100, 100)
        recipe.avatar = db.Blob(avatar)
        recipe.put()
        self.redirect('/?' + urllib.urlencode(
            {'recipe_name': recipe_name}))


application = webapp2.WSGIApplication([('/', MainPage),
                               ('/img', Image),
                               ('/submit', Recipebook)],
                              debug=True)
