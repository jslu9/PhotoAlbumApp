import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.web import (Application, StaticFileHandler, RequestHandler,
                         RedirectHandler, asynchronous, HTTPError)
import json
from models import Session, Albums, Users, Photos
import queries
import models

def get_application(debug=False):
    
    """
    list of web service urls
    """
    
    routes = [
        (r'/album/get/all/?$', AlbumsListHandler),
	(r'/album/get/all/photos/?$', AlbumsPhotosListHandler),
        (r'/album/create/?$', CreateAlbumHandler),
        (r'/album/get/photoId/([^/]+)/?$', GetAlbumsByPhotoHandler),
        (r'/album/delete/?$', DeleteAlbumHandler),
        (r'/user/create/?$', CreateUserHandler),
        (r'/user/delete/?$', DeleteUserHandler),
        (r'/photo/create/?$', CreatePhotoHandler),
        (r'/photo/delete/?$', DeletePhotoHandler),
        (r'/photo/get/albumId/([^/]+)/?$', GetPhotosByAlbumHandler),
        (r'/photoAlbums/init/?$', InitHandler)
    ] 
    return Application(routes, debug=debug)

def run():
    server = HTTPServer(get_application(debug=False))
    server.listen(8888)
    server.start()
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        stop()

def stop():
    tornado.ioloop.IOLoop.current().stop();

"""
The subclasses of AppRequestHandler will inherit the write method which will handle object to json conversion.
"""

class AppRequestHandler(RequestHandler):
    def write(self, input):
        value = json.dumps(input)
        RequestHandler.write(self, value)
        self.set_header('Content-type', 'application/json; charset=utf-8')
        self.finish()

"""
Init request will delete all rows in all tables and then repopulate the rows with all the entities in the albums.json and photos.json files.
"""

class InitHandler(AppRequestHandler):
    def post(self):
        session = Session()
        queries.init(session)
        session.close()
        
"""
Operation to create album
"""

class CreateAlbumHandler(AppRequestHandler):
    def post(self):
        title = self.get_argument('title', '')
        userId = self.get_argument('userId','')
        id = self.get_argument('id', None)
        if not title or not userId:
            results = {"operation": "failed, not all the parameters were set" }
        else:
            session = Session()
            results = queries.create_album(session, title, userId, id)
            session.close()
        self.write(results)

"""
Operation to delete album
"""

class DeleteAlbumHandler(AppRequestHandler):
    def delete(self):
        albumId = self.get_argument('id')
        if not albumId:
            results = {"operation": "failed, not all the parameters were set" }
        else:
            session = Session()
            results = queries.delete_album(session, albumId)
            session.close()
        self.write(results)
 
"""
Operation to get all albums
"""

class AlbumsListHandler(AppRequestHandler):
    def get(self):
	session = Session()
        results = queries.get_albums(session)
        session.close()
        self.write(results)

"""
Operation to get all albums along with their photos 
"""

class AlbumsPhotosListHandler(AppRequestHandler):
    def get(self):
        session = Session()
        results = queries.get_albums_and_photos(session)
        session.close()
        self.write(results)

"""
Operation to get album with the given photo id 
"""

class GetAlbumsByPhotoHandler(AppRequestHandler):
    def get(self, photoId):
        session = Session()
        results = queries.get_albums_by_photo(session, photoId)
        session.close()
        self.write(results)

"""
Operation to create photo and associate it to an album
"""

class CreatePhotoHandler(AppRequestHandler):
    def post(self):
        albumId = self.get_argument('albumId','')
        title = self.get_argument('title','')
        url  = self.get_argument('url','')
        id = self.get_argument('id', None)
        thumbnailUrl = self.get_argument('thumbnailUrl','')
        if not url or not thumbnailUrl or not title or not albumId:
            results = {"operation": "failed, not all the parameters were set" }
        else:
            session = Session()
            results = queries.create_photo(session, albumId, title, url, thumbnailUrl, id)
            session.close()
        self.write(results)

"""
Operation to delete photo
"""

class DeletePhotoHandler(AppRequestHandler):
    def delete(self):
        id = self.get_argument('id','')
        if not id:
            results = {"operation": "failed, not all the parameters were set" }
        else:
            session = Session()
            results = queries.delete_photo(session, id)
            session.close()
        self.write(results)


"""
Operation to get all photos associated to an album
"""

class GetPhotosByAlbumHandler(AppRequestHandler):
    def get(self, albumId):
        session = Session()
        results = queries.get_photos_by_album(session, albumId)
        session.close()
        self.write(results)

"""
Operations to create user
"""

class CreateUserHandler(AppRequestHandler):
    def post(self):
        id = self.get_argument('id', None)
        session = Session()
        results = queries.create_user(session, id)
        session.close()
        self.write(results)

"""
Operation to delete user
"""

class DeleteUserHandler(AppRequestHandler):
    def delete(self):
        id = self.get_argument('id','')
        if not id:
            results = {"operation": "failed, not all the parameters were set" }
        else:
            session = Session()
            results = queries.delete_user(session, id)
            session.close()
        self.write(results)

if __name__ == "__main__":
    run()
