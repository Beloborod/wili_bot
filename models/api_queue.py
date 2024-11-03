from mongoengine import *
from models.connecter import connection
from models.user import UserModel

connection()

available_actions = ["edit_message", "send_message", "delete_message"]


class ApiQueue(Document):
    meta = {"collection": "api_queue"}
    user = ReferenceField(UserModel, required=True)
    can_been_realized = DateTimeField(required=True)
    action = StringField(required=True)
    text = StringField()
    parse_mode = StringField(default="HTML")
    message_id = IntField()
    keyboard = BinaryField()
    callback_key = StringField()
    disable_notification = BooleanField(default=False)

    def clean(self):
        if self.action in available_actions:
            if self.action == "send_message":
                if (self.text is None) or (self.text == ""):
                    raise ValidationError(f"text field must be filled when you send a message")
            if self.action in ["edit_message", "delete_message"]:
                if self.message_id is None:
                    raise ValidationError(f"message_id field required when you edit or delete message")
        else:
            raise ValidationError(f"action field must be one of: {available_actions}")
        if self.parse_mode not in ["HTML", "MARKDOWN"]:
            raise ValidationError(f"Parse mode field must be HTML or MARKDOWN only")
