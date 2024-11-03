from datetime import datetime
from mongoengine import *
from models.connecter import connection
from models.user import UserModel
from configs.system import config as system_config

connection()


class WishModel(Document):
    meta = {"collection": "wishes"}
    name = StringField(required=True, max_length=system_config['max_name_len'])
    owner = ReferenceField(UserModel)
    category = StringField(required=True)
    description = StringField(max_length=system_config['max_description_len'])
    executor = ReferenceField(UserModel)
    completed = BooleanField(default=False)
    create_date = DateTimeField(default=datetime.now())
