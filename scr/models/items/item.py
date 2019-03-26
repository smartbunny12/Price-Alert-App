import uuid
import requests
from bs4 import BeautifulSoup
import re
from scr.common.database import Database
import scr.models.items.constants as ItemConstants
from scr.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url =url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query

        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return '<Item {} with url {}>'.format(self.name, self.url)


    def load_price(self):
        # https://www.amazon.com/Canon-Mark-Frame-Digital-Camera/dp/B01KURGS9E/ref=sr_1_1?crid=YGHA8EE4RGLX&keywords=canon+eos+5d+mark+iv+30.4+mp%2C+body+only%2C+black&qid=1551930296&s=gateway&sprefix=canon+eos+5d%2Cgrocery%2C187&sr=8-1
        #Amazon: <span id="priceblock_ourprice" class="a-size-medium a-color-price">$2,999.00</span>

        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, 'html.parser')

        element = soup.find(self.tag_name, self.query) # element: <span class='now-price' itemprop = 'price'>
        string_price = element.text.strip()

        pattern = re.compile('(\d+.\d+)')  #$115.00
        match =pattern.search(string_price) # <_sre.SRE_Match object; span =(1,6), match ='45.00'>
        self.price = float(match.group())

        return self.price


    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'id':self._id}, self.json())


    def json(self):
        return{
            '_id':self._id,
            'name':self.name,
            'url':self.url,
            'price':self.price
        }

    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION,{'_id':item_id}))