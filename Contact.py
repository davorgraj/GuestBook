from google.appengine.ext import ndb


class ContactBook(ndb.Model):
    name_surname = ndb.StringProperty()
    email = ndb.StringProperty()
    text = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
