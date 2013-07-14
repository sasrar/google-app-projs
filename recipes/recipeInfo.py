from models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

# This class operates when user clicks on a recipe on the list
# This class shows a new page with recipe details
class RecipeInfo(webapp2.RequestHandler):
  def get(self):
    recipe = db.get(self.request.get('recipe_id'))
    
    template_values = {'recipe': recipe}
    
    template = JINJA_ENVIRONMENT.get_template('recipe.html')
    self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([('/recipeInfo', RecipeInfo)],debug=True)
