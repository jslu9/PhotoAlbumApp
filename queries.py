from models import Albums, Photos, Users
import json
import settings

def get_photos_by_album(dbsession, albumId):
    result = dbsession.query(Photos).filter(Photos.albumId == albumId).all()
    return [{'id': x.id, 'albumId': x.albumId, 'title': x.title, 'url': x.url} for x in result] 

def get_albums_by_photo(dbsession, photoId):
    result = dbsession.query(Albums).join(Photos, Photos.albumId == Albums.id).filter(Photos.id == photoId).all()
    return [{'id': x.id, 'userId': x.userId, 'title': x.title} for x in result]

def get_albums_and_photos(dbsession):
    result = dbsession.query(Albums.id, Albums.userId, Albums.title).all()
    return [ {'Album Id': x[0], 'User Id': x[1], 'Album title': x[2], 'Photos': [{'Photo Id': y.id, 'Photo title': y.title} for y in dbsession.query(Photos).filter(Photos.albumId == x[0]).all()]} for x in result]

def create_photo(dbsession, albumId, title, url):
    newPhoto = Photos(albumId = albumId, title = title, url= url)
    dbsession.add(newPhoto)
    dbsession.commit()
    return {"operation": "success"}

def delete_photo(dbsession, id):
    photo = Photo(id=id)
    dbsession.delete(photo)
    dbsession.commit()
    return {"operation": "success"}

def create_album(dbsession, title, userId):
    newAlbum = Albums(title = title, userId = userId)
    dbsession.add(newAlbum)
    dbsession.commit()
    return {"operation": "success"}

def delete_user(dbsession, id):
    dbsession.query(Users).filter(Users.id == id).\
    delete(synchronize_session=False)
    dbsession.commit()
    return {"operation": "success"}

def get_albums(dbsession):
    result = dbsession.query(Albums).all()
    return [{'id': x.id, 'userId': x.userId, 'title': x.title} for x in result] 

def create_user(dbsession):
    newUser = Users()
    dbsession.add(newUser)
    dbsession.commit()
    return {"operation": "success"}

def empty_tables(dbsession):
    dbsession.query(Photos).delete()
    dbsession.commit()
    dbsession.query(Albums).delete()
    dbsession.commit()
    dbsession.query(Users).delete()
    dbsession.commit()

def init(dbsession):
    empty_tables(dbsession)
    for x in range(1, 11):
        dbsession.add(Users())
        dbsession.commit()

    with open(settings.photos_json) as f:
        data=f.read()
        photos_json_data=json.loads(data)

    with open(settings.albums_json) as f:
        data=f.read()
        albums_json_data=json.loads(data)

    for obj in albums_json_data:
        dbsession.add(Albums(id=obj['id'], title=obj['title'], userId=obj['userId']))
        dbsession.commit()

    for obj in photos_json_data:
        dbsession.add(Photos(id=obj['id'], title=obj['title'], albumId=obj['albumId'], url=obj['url'], thumbnailUrl=obj['thumbnailUrl']))
        dbsession.commit()
