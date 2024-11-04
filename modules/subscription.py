import mongoengine.errors
import telebot.types
from configs.constants import config as constants
from configs.messages import config as messages_texts
from models.user import UserModel
from models.wish import WishModel
from modules.system import format_text
from modules.telegram_bot import TgBot
from configs.system import config as system_config


async def subscribe(bot: TgBot, user: UserModel, target_id: int):
    if len(user.subscribes) > system_config['max_subscribes']:
        await bot.add_message_to_queue(user.user_id, format_text(messages_texts["max_subscribes"],
                                                                 variables={"cnt": system_config['max_subscribes']}))
        return
    try:
        target_user = UserModel.objects.get(user_id=target_id)
    except mongoengine.errors.DoesNotExist:
        await bot.add_message_to_queue(user.user_id, format_text(messages_texts["cant_subscribe"]))
        return
    if target_user in user.subscribes:
        await bot.add_message_to_queue(user.user_id, format_text(messages_texts["already_subscribe"]))
        return
    user.subscribes.append(target_user)
    user.save()

    if user in target_user.subscribes:
        user.subscribes.append(target_user)
        user.save()
        await bot.add_message_to_queue(user.user_id, format_text(messages_texts["subscribe_friend"],
                                                                 {
                                                                     "f_n": target_user.f_n,
                                                                     "l_n": target_user.l_n if target_user.l_n else "",
                                                                     "user_id": target_user.user_id
                                                                 }))
        await bot.add_message_to_queue(target_user.user_id, format_text(messages_texts["subscribe_friend"],
                                                                        {
                                                                            "f_n": user.f_n,
                                                                            "l_n": user.l_n if user.l_n
                                                                            else "",
                                                                            "user_id": user.user_id
                                                                        }))
    else:
        if target_user.private:
            await bot.add_message_to_queue(user.user_id, format_text(messages_texts["subscribe_private"],
                                                                     {
                                                                         "f_n": target_user.f_n,
                                                                         "l_n": target_user.l_n if target_user.l_n
                                                                         else "",
                                                                         "user_id": target_user.user_id
                                                                     }))
        else:
            await bot.add_message_to_queue(user.user_id, format_text(messages_texts["subscribe_any"],
                                                                     {
                                                                         "f_n": target_user.f_n,
                                                                         "l_n": target_user.l_n if target_user.l_n
                                                                         else "",
                                                                         "user_id": target_user.user_id
                                                                     }))


def unsubscribe(user: UserModel, target: UserModel):
    user.subscribes.remove(target)
    user.save()

    wishes = WishModel.objects(executor=user, owner=target)

    for wish in wishes:
        if wish.executor == user:
            wish.executor = None
            wish.save()

    wishes = WishModel.objects(executor=target)
    for wish in wishes:
        if wish.executor == target:
            wish.executor = None
            wish.save()


def get_friends_keyboard(user: UserModel, cur_offset: int = 0):
    friends = user.subscribes

    if len(friends) == 0:
        return False

    keyboard = telebot.types.InlineKeyboardMarkup()
    new_friends_list = friends[cur_offset : cur_offset + system_config["pagination"]]
    if len(new_friends_list) == 0:
        new_friends_list = friends[:system_config["pagination"]]

    for friend in new_friends_list:
        keyboard.add(telebot.types.InlineKeyboardButton(friend.f_n + " " + friend.l_n,
                                                        callback_data=f"friend:{friend.id}:look"),
                     telebot.types.InlineKeyboardButton(constants["unsubscribe"],
                                                        callback_data=f"friend:{friend.id}:delete")
                     )
    row = []
    if len(friends[cur_offset - system_config['pagination'] : cur_offset]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["back"],
                                                        callback_data=f"friend:"
                                                                      f"{cur_offset - system_config['pagination']}:"
                                                                      f"list"))

    if len(friends[cur_offset + system_config["pagination"] : cur_offset + system_config["pagination"] * 2]) > 0:
        row.append(telebot.types.InlineKeyboardButton(constants["forward"],
                                                        callback_data=f"friend:"
                                                                      f"{cur_offset + system_config['pagination']}:"
                                                                      f"list"))
    keyboard.add(*row)
    return keyboard

def get_friend_message_keyboard(user: UserModel, friend_id: str):
    keyboard = telebot.types.InlineKeyboardMarkup()
    friend = UserModel.objects.get(id=friend_id)
    if friend.private and (not (user in friend.subscribes)):
        mes = format_text(messages_texts['friend_private'],
                           {
                               "f_n": friend.f_n,
                               "l_n": friend.l_n,
                               "user_id": friend.user_id
                           })
    else:
        for category, wishes in friend.wishes.items():
            keyboard.add(telebot.types.InlineKeyboardButton(format_text(category) + f" ({len(wishes)})",
                                                            callback_data=f"friend:{friend.id}:{category}:0:category"))
        mes = format_text(messages_texts['friend_categories'],
                          {
                              "f_n": friend.f_n,
                              "l_n": friend.l_n,
                              "user_id": friend.user_id
                          })
    keyboard.add(telebot.types.InlineKeyboardButton(constants["step_back"],
                                                    callback_data=f"friend:0:list"))
    return mes, keyboard