import re
from typing import List
import telebot.types
from configs.constants import config as constants
from models.user import UserModel
from modules.telegram_bot import TgBot
from configs.messages import config as messages_texts
from configs.system import config as system_config


def format_text(text: str, variables: dict = None):
    if variables:
        constants.update(variables)
    return text.format(**constants)


async def cancel_action(bot: TgBot, user: UserModel):
    user.status = system_config['default_status']
    user.save()
    await bot.add_message_to_queue(user.user_id, format_text(messages_texts['cancel']))


def cancel_keyboard(keys: List[telebot.types.InlineKeyboardButton] = None):
    keyboard = telebot.types.InlineKeyboardMarkup()
    if keys:
        for key in keys:
            keyboard.add(key)
    keyboard.add(telebot.types.InlineKeyboardButton(constants['cancel'], callback_data="cancel"))
    return keyboard


def check_text(text: str):
    if re.match(r".*([{}]).*", text):
        return False
    else:
        return True

def settings_keyboard(user: UserModel):
    mes = format_text(messages_texts['settings'],
                      {
                          'notifications_status': constants['on'] if user.notifications else constants['off'],
                          'private_status': constants['on'] if user.private else constants['off'],
                          'clear_chat_status':  constants['on'] if user.clear_chat else constants['off']
                      })
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(
        format_text("{notifications}: {notifications_status}",
                    {'notifications_status': constants['on'] if user.notifications else constants['off']}),
    callback_data="settings:notifications"))
    keyboard.add(telebot.types.InlineKeyboardButton(
        format_text("{private}: {private_status}",
                    {'private_status': constants['on'] if user.private else constants['off']}),
    callback_data="settings:private"))
    keyboard.add(telebot.types.InlineKeyboardButton(
        format_text("{clear_chat}: {clear_chat_status}",
                    {'clear_chat_status': constants['on'] if user.clear_chat else constants['off']}),
    callback_data="settings:clear_chat"))
    return mes, keyboard
