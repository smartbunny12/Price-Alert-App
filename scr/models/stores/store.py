import uuid

from scr.common.database import Database
import scr.models.stores.constants as StoreConstants
import scr.models.stores.errors as StoreErrors

class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        # usually the url for an item are under the same store url prefix, so we can know which store the item in
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return '<Store {}>'.format(self.name)


    def json(self):
        return{
            '_id': self._id,
            'name':self.name,
            'url_prefix':self.url_prefix,
            'tag_name':self.tag_name,
            'query':self.query
        }



    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'_id':id}))



    def save_to_mongo(self):
        Database.insert(StoreConstants.COLLECTION, self.json())


    @classmethod
    def get_by_name(cls,store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'name':store_name}))



    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        http://www.johnlewis<-  {id:..., name:'John Lewis'...}
        :param url_prefix:
        :return:
        """
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'url_prefix':{'$regex':'^{}'.format(url_prefix)}}))


    @classmethod
    def find_by_url(cls, url):
        """
        return a store from a url
        :param url: the item's url
        :return: store, if no store found, return exception
        """
        for i in range(len(url)):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The url Prefix used to find store didn't give us any result")


    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]





