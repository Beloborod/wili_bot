import re
from configs.system import config as system_config
import mongoengine.errors
import telebot.types
from models.user import UserModel
from modules.subscription import subscribe
from modules.system import check_text, cancel_keyboard, format_text
from modules.telegram_bot import TgBot
from configs.constants import config as constants
from configs.messages import config as messages_texts
from modules.wishes import save_wish


async def message_coordinator(bot: TgBot, message: telebot.types.Message):
    user = UserModel.objects.get(user_id=message.from_user.id)
    subscribe_id = None

    await bot.add_message_to_queue(message.chat.id, message_id=message.message_id, action="delete_message")

    if user.status['state'] == "subscribe":
        if message.forward_origin:
            if message.forward_origin.type == "user":
                subscribe_id = message.forward_origin.sender_user.id
        elif re.match(r"^@\S*$", message.text):
            try:
                sub_target = UserModel.objects.get(acc_name__iexact=message.text[1:])
                subscribe_id = sub_target.user_id
            except mongoengine.errors.DoesNotExist:
                await bot.add_message_to_queue(user.user_id, format_text(messages_texts["cant_subscribe"]))
        user.status["state"] = "idle"
        user.save()
        if subscribe_id:
            await subscribe(bot, user, subscribe_id)

    if user.status['state'] == "add_wish":
        if user.status['sub_info'] == "name":
            if check_text(message.text):
                if len(message.text) > system_config['max_name_len']:
                    await bot.add_message_to_queue(message.chat.id, text=format_text(messages_texts['too_long_name']))
                    return
                user.status['wish_name'] = message.text
                user.status['sub_info'] = "description"
                user.save()
                keyboard = cancel_keyboard([telebot.types.InlineKeyboardButton(constants['accept'],
                                                                               callback_data="wish:accept")])
                await bot.add_message_to_queue(message.chat.id,
                                               text=format_text(messages_texts['wish_description'],
                                                                variables={
                                                                    "wish_name": user.status['wish_name'],
                                                                    "wish_description": user.status['wish_description'],
                                                                    "wish_category": format_text(
                                                                        user.status['wish_category'])
                                                                }),
                                               reply_markup=keyboard)
            else:
                await bot.add_message_to_queue(message.chat.id, text=format_text(messages_texts['wrong_symbols']))
        elif user.status['sub_info'] == "description":
            if check_text(message.text):
                if len(message.text) > system_config['max_description_len']:
                    await bot.add_message_to_queue(message.chat.id,
                                                   text=format_text(messages_texts['too_long_description']))
                    return
                user.status['wish_description'] = message.text
                wish = await save_wish(bot, user)
                await bot.add_message_to_queue(message.chat.id,
                                               text=format_text(messages_texts['saved_wish'],
                                                                {
                                                                    "wish_name": wish.name,
                                                                    "wish_category": format_text(wish.category),
                                                                    "wish_description": wish.description
                                                                }))
            else:
                await bot.add_message_to_queue(message.chat.id, text=format_text(messages_texts['wrong_symbols']))
