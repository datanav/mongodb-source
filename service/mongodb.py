import pymongo
import datetime
import json
from bson import ObjectId
from datetime import datetime


# encode MongoDB BSON as JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o.strftime("%Y-%m-%dT%H:%M:%SZ"))
        return json.JSONEncoder.default(self, o)


class MongoDB(object):

    # FIXME: authentication with secret
    def __init__(self, host, port, database, username=None, password=None, secret=None):
        self._client = pymongo.MongoClient('mongodb://{host}:{port}'
                                           ''.format(host=host, port=port))
        self._db = self._client[database]
#        self._db.authenticate(username, password)

    def __get_all_entities(self, collection):

        for entity in self._db[collection].find():
            return JSONEncoder().encode(entity)

    def __get_all_entities_since(self, collection, since):
        # FIXME
        # 2017-03-16T10:15:15.677000
        dt = datetime.strptime(since, '%Y-%m-%dT%H:%M:%S.%f')
        print('parsed date', repr(dt))
        for entity in self._db[collection].find({'lastModified': {'$gt': dt}}):
            return JSONEncoder().encode(entity)

    def get_entities(self, collection, since=None):
        if since is None:
            print('getting all')
            return self.__get_all_entities(collection)
        else:
            print('getting since', since)
            return self.__get_all_entities_since(collection, since)