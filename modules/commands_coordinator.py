import telebot.types
from models.user import UserModel
from modules.telegram_bot import TgBot
from configs.messages import config as messages_texts
from modules.system import format_text, cancel_action, cancel_keyboard
from modules.wishes import get_wishes_accepted_keyboard, get_category_keyboard
from modules.subscription import get_friends_keyboard


async def command_coordinator(bot: TgBot, message: telebot.types.Message):
    command = message.text.split(" ")[0][1:]
    args = message.text.split(" ")[1:]
    user = UserModel.objects.get(user_id=message.from_user.id)

    if command == "cancel":
        await cancel_action(bot, user)
        return

    if user.status['state'] == "subscribe":
        await cancel_action(bot, user)
        user.reload()

    if user.status['state'] == "idle":
        if command == "start":
            await bot.add_message_to_queue(message.chat.id, format_text(messages_texts['start']))
        elif command == "wish":
            keyboard = get_category_keyboard(user, "add_wish")
            await bot.add_message_to_queue(message.chat.id, format_text(messages_texts['wish']), reply_markup=keyboard)
        elif command == "help":
            await bot.add_message_to_queue(message.chat.id, format_text(messages_texts['help']))
        elif command == "subscribe":
            user.status['state'] = "subscribe"
            user.save()
            keyboard = cancel_keyboard()
            await bot.add_message_to_queue(message.chat.id, format_text(messages_texts['subscribe']),
                                           reply_markup=keyboard)
        elif command == "wishes":
            await bot.add_message_to_queue(message.chat.id, format_text(messages_texts['choose_category']),
                                           reply_markup=get_category_keyboard(user, "0:look"))
        elif command == "accepted":
            await bot.add_message_to_queue(message.chat.id,
                                           format_text(messages_texts['look_accepted_wishes'],
                                                       {
                                                           "wish_category": "",
                                                           "wish_name": "",
                                                           "wish_description": "",
                                                           "f_n": "",
                                                           "l_n": "",
                                                           "user_id": None
                                                       }),
                                           reply_markup=get_wishes_accepted_keyboard(user))
        elif command == "friends":
            await bot.add_message_to_queue(message.chat.id,
                                           format_text(messages_texts['friends_list']),
                                           reply_markup=get_friends_keyboard(user))
        elif command == "private":
            user.private = not user.private
            user.save()
            await bot.add_message_to_queue(message.chat.id,
                                           format_text(messages_texts['private_true'] if user.private
                                                       else messages_texts['private_false']))
