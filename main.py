#!/usr/bin/env python
import os
import jinja2
import webapp2
from Contact import ContactBook

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        name_surname = self.request.get("name_surname")
        email = self.request.get("email")
        message = self.request.get("message")

        if not name_surname:
            name_surname = "Neznanec"

        cb_object = ContactBook(name_surname=name_surname, email=email, text=message.replace("<script>", ""))
        cb_object.put()
        
        return self.render_template("hello.html")


class AllContactMessagesHandler(BaseHandler):
    def get(self):
        all_contact_book = ContactBook.query().fetch()

        params = {"all_contact": all_contact_book}

        return self.render_template("seznam.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/seznam', AllContactMessagesHandler),
], debug=True)
