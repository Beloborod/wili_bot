from typing import List
import mongoengine
import telebot.types
from configs.constants import config as constants
from models.user import UserModel
from models.wish import WishModel
from configs.system import config as system_config
from modules.system import format_text, cancel_action
from modules.telegram_bot import TgBot
from configs.messages import config as messages_texts


async def save_wish(bot: TgBot, user: UserModel):
    if 'wish_id' in user.status.keys():
        try:
                wish = WishModel(id=user.status['wish_id'])
        except mongoengine.errors.DoesNotExist:
            await cancel_action(bot, user)
            return
    else:
        wish = WishModel()
    wish.name = user.status['wish_name']
    wish.description = user.status['wish_description']
    wish.owner = user
    category = user.status['wish_category']
    wish.category = category
    wish.save()
    user.wishes[category].append(wish)
    user.status = system_config['default_status']
    user.save()
    await send_new_wish(bot, user, wish)
    return wish


async def send_new_wish(bot: TgBot, user: UserModel, wish: WishModel):
    subscribers = UserModel.objects(subscribes__contains=user)
    for sub in subscribers:
        if sub in user.subscribes:
            await bot.add_message_to_queue(sub.user_id, format_text(messages_texts["new_wish"],
                                                                    {
                                                                        "f_n": user.f_n,
                                                                        "l_n": user.l_n,
                                                                        "user_id": user.user_id,
                                                                        "wish_name": wish.name,
                                                                        "wish_description": wish.description,
                                                                        "wish_category": format_text(wish.category)
                                                                    }), reply_markup=get_wish_keyboard(wish.id))
        elif not user.private:
            await bot.add_message_to_queue(sub.user_id, format_text(messages_texts["new_wish"],
                                                                    {
                                                                        "f_n": user.f_n,
                                                                        "l_n": user.l_n,
                                                                        "user_id": user.user_id,
                                                                        "wish_name": wish.name,
                                                                        "wish_description": wish.description,
                                                                        "wish_category": format_text(wish.category)
                                                                    }))


def get_wish_keyboard(wish_id: mongoengine.ObjectIdField):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(constants['execute_wish'], callback_data=f"execute_wish:{wish_id}"))
    return keyboard

def get_wishes_owner_keyboard(wishes: List[WishModel], cur_offset: int = 0):
    if len(wishes) == 0:
        return False

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    new_wishes_list = wishes[cur_offset : cur_offset + system_config["pagination"]]
    if len(new_wishes_list) == 0:
        new_wishes_list = wishes[:system_config["pagination"]]

    for wish in new_wishes_list:
        keyboard.add(telebot.types.InlineKeyboardButton(wish.name, callback_data=f"wish:{wish.id}:look"),
                     telebot.types.InlineKeyboardButton(constants["delete"], callback_data=f"wish:{wish.id}:delete"),
                     telebot.types.InlineKeyboardButton(constants["edit"], callback_data=f"wish:{wish.id}:edit"),
                     telebot.types.InlineKeyboardButton(constants["realize"], callback_data=f"wish:{wish.id}:realized")
                     )
    row = []
    if len(wishes[cur_offset - system_config['pagination'] : cur_offset]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["back"],
                                                        callback_data=f"category:"
                                                                      f"{wishes[0].category}:"
                                                                      f"{cur_offset - system_config['pagination']}:"
                                                                      f"look"))

    row.append(telebot.types.InlineKeyboardButton(constants["step_back"], callback_data="category:list"))

    if len(wishes[cur_offset + system_config["pagination"] : cur_offset + system_config["pagination"] * 2]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["forward"],
                                                        callback_data=f"category:{wishes[0].category}:"
                                                                      f"{cur_offset + system_config['pagination']}:"
                                                                      f"look"))
    keyboard.add(*row)
    return keyboard


def get_wishes_accepted_keyboard(user: UserModel, cur_offset: int = 0):
    wishes = WishModel.objects(completed=False, executor=user)
    if len(wishes) == 0:
        return False

    keyboard = telebot.types.InlineKeyboardMarkup()
    new_wishes_list = wishes[cur_offset : cur_offset + system_config["pagination"]]
    if len(new_wishes_list) == 0:
        new_wishes_list = wishes[:system_config["pagination"]]

    for wish in new_wishes_list:
        keyboard.add(telebot.types.InlineKeyboardButton(wish.name, callback_data=f"accepted:{wish.id}:look"),
                     telebot.types.InlineKeyboardButton(constants["refuse"], callback_data=f"accepted:{wish.id}:delete")
                     )
    row = []
    if len(list(wishes)[cur_offset - system_config['pagination'] : cur_offset]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["back"],
                                                        callback_data=f"accepted:"
                                                                      f"{cur_offset - system_config['pagination']}:"
                                                                      f"list"))

    if len(list(wishes)[cur_offset + system_config["pagination"] : cur_offset + system_config["pagination"] * 2]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["forward"],
                                                        callback_data=f"accepted:"
                                                                      f"{cur_offset + system_config['pagination']}:"
                                                                      f"list"))
    keyboard.add(*row)
    return keyboard


def get_category_keyboard(user: UserModel, action: str):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for wish_category, wishes in user.wishes.items():
        keyboard.add(telebot.types.InlineKeyboardButton(format_text(wish_category) + f" ({len(wishes)})",
                                                        callback_data=f"category:{wish_category}:{action}"))
    return keyboard

def get_friend_wishes_keyboard(user: UserModel, friend_id: str, category: str, cur_offset: int = 0):
    friend = UserModel.objects.get(id=friend_id)
    if friend.private and (not (user in friend.subscribes)):
        return False

    wishes = friend.wishes[category] if category in friend.wishes.keys() else []

    # if len(wishes) == 0:
    #     return False

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    new_wishes_list = wishes[cur_offset : cur_offset + system_config["pagination"]]
    if len(new_wishes_list) == 0:
        new_wishes_list = wishes[:system_config["pagination"]]

    for wish in new_wishes_list:
        row = [telebot.types.InlineKeyboardButton(wish.name, callback_data=f"friend:{wish.id}:{cur_offset}:wish")]
        if user in friend.subscribes:
            if not wish.executor:
                row.append(telebot.types.InlineKeyboardButton(constants["execute"],
                                                              callback_data=f"wish:{wish.id}:{cur_offset}:execute"))
            elif wish.executor == user:
                row.append(telebot.types.InlineKeyboardButton(constants["refuse"],
                                                              callback_data=f"wish:{wish.id}:{cur_offset}:refuse"))
        keyboard.add(*row)
    row = []
    if len(wishes[cur_offset - system_config['pagination'] : cur_offset]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["back"],
                                                        callback_data=f"friend:"
                                                                      f"{friend_id}:"
                                                                      f"{category}:"
                                                                      f"{cur_offset - system_config['pagination']}:"
                                                                      f"category"))

    row.append(telebot.types.InlineKeyboardButton(constants["step_back"], callback_data=f"friend:{friend_id}:look"))

    if len(wishes[cur_offset + system_config["pagination"] : cur_offset + system_config["pagination"] * 2]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["forward"],
                                                        callback_data=f"friend:"
                                                                      f"{friend_id}:"
                                                                      f"{category}:"
                                                                      f"{cur_offset + system_config['pagination']}:"
                                                                      f"category"))
    keyboard.add(*row)
    return keyboard
