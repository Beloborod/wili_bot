from mongoengine import *
from models.connecter import connection
from models.user import UserModel

connection()

available_actions = ["edit_message", "send_message", "delete_message"]


class QueueCallback(Document):
    meta = {"collection": "queue_callback", "timeseries": {"expireAfterSeconds": 172800}}
    user = ReferenceField(UserModel, required=True)
    key = StringField(required=True)
    returned = BinaryField()
    message_id = StringField()
    message_text = StringField()
    message_inline_keyboard = BinaryField()
    expireAfterSeconds = IntField()
