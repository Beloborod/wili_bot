import telebot.types
from models.user import UserModel
from modules.subscription import subscribe
from modules.telegram_bot import TgBot


async def contact_coordinator(bot: TgBot, message: telebot.types.Message):
    user = UserModel.objects.get(user_id=message.from_user.id)
    if user.status['state'] == "subscribe":
        user.status['state'] = "idle"
        user.save()
        subscribe_id = message.contact.user_id
        await subscribe(bot, user, subscribe_id)