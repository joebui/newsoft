from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import images
import os
import logging
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

# Object model
class Category(ndb.Model):
    name = ndb.StringProperty()

class News(ndb.Model):
    category = ndb.KeyProperty(kind=Category)
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    datetime_created = ndb.DateTimeProperty(auto_now_add=True)
    date_created = ndb.DateProperty(auto_now_add=True)

# Back-end functions
class DefaultPage(webapp2.RequestHandler):
    def get(self):
        self.redirect('/home')

class HomePage(webapp2.RequestHandler):
    def get(self):
        ID = self.request.get('category')
        if ID:
            key = ndb.Key("Category", int(ID))
            news = News.query(News.category == key).order(-News.date_created)
        else:
            news = News.query().order(-News.date_created)

        l_news = News.query().order(-News.datetime_created)
        latest = l_news.fetch(1)

        cate = Category.query()

        template_values = {
            'news': news,
            'l_news': l_news,
            'latest': latest,
            'cate': cate,
        }

        template = JINJA_ENVIRONMENT.get_template('/templates/homepage.html')
        self.response.write(template.render(template_values))

class NewsDetails(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("News", int(self.request.get('id')))
        news = News.query(News.key == key).get()
        cate = Category.query(Category.key == news.category).get()

        template_values = {
            'news': news,
            'cate': cate,
        }

        template = JINJA_ENVIRONMENT.get_template('/templates/news_details.html')
        self.response.write(template.render(template_values))

class AdminIndex(webapp2.RequestHandler):
    def get(self):
        news = News.query().order(-News.date_created)
        cate = Category.query()

        template_values = {
            'news': news,
            'cate': cate,
        }

        template = JINJA_ENVIRONMENT.get_template('/templates/admin_index.html')
        self.response.write(template.render(template_values))

    def delete(self, ID):
        key = ndb.Key("News", int(ID))
        news = News.query(News.key == key).get()
        news.key.delete()
        self.response.write('ok')

class AdminAddNews(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/admin_add.html')
        self.response.write(template.render())

    def post(self):
        cate_name = self.request.get('group')
        cate = Category.query(Category.name == cate_name).get()

        if not cate:
            cate = Category()
            cate.name = cate_name.replace(' ', '_')
            cate.put()

        news = News()
        news.category = cate.key
        news.title = self.request.get('title')
        news.content = self.request.get('editor1')
        news.put()

        self.redirect('/home')

class AdminEditNews(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key("News", int(self.request.get('id')))
        news = News.query(News.key == key).get()
        cate = Category.query(Category.key == news.category).get()

        template_values = {
            'required_news': news,
            'cate': cate,
        }

        template = JINJA_ENVIRONMENT.get_template('/templates/admin_edit.html')
        self.response.write(template.render(template_values))

    def post(self, ID):
        key = ndb.Key("News", int(ID))

        cate_name = self.request.get('group')
        cate = Category.query(Category.name == cate_name).get()

        if not cate:
            cate = Category()
            cate.name = cate_name.replace(' ', '_')
            cate.put()

        news = News.query(News.key == key).get()
        news.category = cate.key
        news.title = self.request.get('title')
        news.content = self.request.get('editor1')
        news.put()

        self.redirect('/home')

application = webapp2.WSGIApplication([
    ('/', DefaultPage),
    ('/home', HomePage),
    (r'/home/(\w+)', HomePage),
    ('/details', NewsDetails),
    (r'/details/(\w+)', NewsDetails),
    ('/index', AdminIndex),
    (r'/index/(\w+)', AdminIndex),
    ('/new', AdminAddNews),
    ('/edit', AdminEditNews),
    (r'/edit/(\w+)', AdminEditNews),
], debug = True)
