import mongoengine.errors
import telebot.types
from telebot.types import InlineKeyboardButton
from configs.constants import config as constants
from configs.messages import config as messages_texts
from models.user import UserModel
from models.wish import WishModel
from modules.subscription import get_friends_keyboard, get_friend_message_keyboard, unsubscribe
from modules.system import format_text, cancel_keyboard, cancel_action, check_text
from modules.telegram_bot import TgBot
from modules.wishes import get_wishes_owner_keyboard, save_wish, get_friend_wishes_keyboard, \
    get_wishes_accepted_keyboard, get_category_keyboard


async def callback_coordinator(bot: TgBot, call: telebot.types.CallbackQuery):
    data = call.data.split(":")
    user = UserModel.objects.get(user_id=call.from_user.id)
    if data[0] == "cancel":
        await bot.add_message_to_queue(call.message.chat.id, action="delete_message",
                                       message_id=call.message.message_id)
        await cancel_action(bot, user)

    elif user.status['state'] == "idle":
        if data[0] == "category":
            if data[-1] == "add_wish":
                user = UserModel.objects.get(user_id=call.from_user.id)
                user.status['state'] = "add_wish"
                user.status['wish_category'] = data[1]
                user.status['wish_name'] = ""
                user.status['wish_description'] = ""
                user.status['wish_id'] = None
                user.status['sub_info'] = "name"
                user.save()
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['choose_wish_name'],
                                                           variables={
                                                               "wish_name": user.status['wish_name'],
                                                               "wish_description": user.status['wish_description'],
                                                               "wish_category": format_text(
                                                                   user.status['wish_category'])
                                                           }),
                                               action="edit_message", reply_markup=cancel_keyboard(),
                                               message_id=call.message.message_id)
            elif data[-1] == "look":
                keyboard = get_wishes_owner_keyboard(user.wishes[data[1]], int(data[2]))
                if not keyboard:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['empty_category']),
                                                   action="edit_message", message_id=call.message.message_id)
                else:
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['look_wishes'],
                                                               variables={
                                                                   "wish_category": format_text(data[1]),
                                                                   "wish_name": "",
                                                                   "wish_description": ""
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id,
                                                   reply_markup=keyboard)
            elif data[-1] == "list":
                await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['choose_category']),
                                               reply_markup=get_category_keyboard(user, "0:look"),
                                               action="edit_message", message_id=call.message.message_id)

        elif data[0] == "execute_wish":
            try:
                wish = WishModel.objects.get(id=data[1], completed=False, executor=None)
            except mongoengine.errors.DoesNotExist:
                await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                               action="edit_message", message_id=call.message.message_id)
                return
            if user in wish.owner.subscribes:
                wish.executor = user
                wish.save()
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['wish_execute'],
                                                           variables={
                                                               "f_n": wish.owner.f_n,
                                                               "l_n": wish.owner.l_n,
                                                               "user_id": wish.owner.user_id,
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                           }),
                                               action="edit_message", message_id=call.message.message_id)

        elif data[0] == "wish":
            if data[-1] == "edit":
                try:
                    wish = WishModel.objects.get(id=data[1], completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                user.status['state'] = "add_wish"
                user.status['wish_category'] = wish.category
                user.status['wish_name'] = wish.name
                user.status['wish_description'] = wish.description
                user.status['wish_id'] = wish.id
                user.status['sub_info'] = "name"
                user.save()
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['choose_wish_name'],
                                                           variables={
                                                               "wish_name": user.status['wish_name'],
                                                               "wish_description": user.status['wish_description'],
                                                               "wish_category": format_text(
                                                                   user.status['wish_category'])
                                                           }
                                                           ),
                                               action="edit_message",
                                               reply_markup=cancel_keyboard([telebot.types.InlineKeyboardButton(
                                                   text=constants['accept'],
                                                   callback_data="wish:accept"
                                               )]),
                                               message_id=call.message.message_id)
            elif data[-1] == "delete":
                try:
                    wish = WishModel.objects.get(id=data[1], completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['accept_delete'],
                                                           {
                                                               "wish_category": format_text(wish.category),
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                               "executing": constants['executed'] if wish.executor
                                                               else constants['not_executed']
                                                           }),
                                               reply_markup=cancel_keyboard(
                                                   [telebot.types.InlineKeyboardButton(
                                                       constants['delete'],
                                                       callback_data=f"wish:{data[1]}:delete_acc")]),
                                               action="edit_message", message_id=call.message.message_id)
            elif data[-1] == "delete_acc":
                try:
                    wish = WishModel.objects.get(id=data[1], completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                mes = format_text(messages_texts['wish_deleted'], variables={
                    "wish_category": format_text(wish.category),
                    "wish_name": wish.name,
                    "wish_description": wish.description,
                    "f_n": user.f_n,
                    "l_n": user.l_n,
                    "user_id": user.user_id
                })
                if wish.executor:
                    await bot.add_message_to_queue(wish.executor.user_id, mes)
                await bot.add_message_to_queue(call.message.chat.id, mes, action="edit_message",
                                               message_id=call.message.message_id)
                user.wishes[wish.category].remove(wish)
                user.save()
                wish.delete()
            elif data[-1] == "realized":
                try:
                    wish = WishModel.objects.get(id=data[1], completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['accept_realize'],
                                                           {
                                                               "wish_category": format_text(wish.category),
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                               "executing": constants['executed'] if wish.executor
                                                               else constants['not_executed']
                                                           }),
                                               reply_markup=cancel_keyboard(
                                                   [telebot.types.InlineKeyboardButton(
                                                       constants['accept'],
                                                       callback_data=f"wish:{data[1]}:realize_acc")]),
                                               action="edit_message", message_id=call.message.message_id)
            elif data[-1] == "realize_acc":
                try:
                    wish = WishModel.objects.get(id=data[1], completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                mes = format_text(messages_texts['wish_realized'], variables={
                    "wish_category": format_text(wish.category),
                    "wish_name": wish.name,
                    "wish_description": wish.description,
                    "f_n": user.f_n,
                    "l_n": user.l_n,
                    "user_id": user.user_id
                })
                if wish.executor:
                    await bot.add_message_to_queue(wish.executor.user_id, mes)
                await bot.add_message_to_queue(call.message.chat.id, mes, action="edit_message",
                                               message_id=call.message.message_id)
                wish.completed = True
                wish.save()
                user.wishes[wish.category].remove(wish)
                user.save()
            elif data[-1] == "refuse":
                try:
                    wish = WishModel.objects.get(id=data[1], executor=user, completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                wish.executor = None
                wish.save()
                keyboard = get_friend_wishes_keyboard(user, wish.owner.id, wish.category, int(data[2]))
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['friend_wishes'],
                                                           {
                                                               "f_n": wish.owner.f_n,
                                                               "l_n": wish.owner.l_n,
                                                               "user_id": wish.owner.user_id,
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                               "executing": constants['executed'] if wish.executor
                                                               else constants['not_executed']
                                                           }), reply_markup=keyboard,
                                               action="edit_message", message_id=call.message.message_id)
            elif data[-1] == "execute":
                try:
                    wish = WishModel.objects.get(id=data[1], executor=None, completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                if not (user in wish.owner.subscribes):
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['friend_private'],
                                                               {
                                                                   "f_n": wish.owner.f_n,
                                                                   "l_n": wish.owner.l_n,
                                                                   "user_id": wish.owner.user_id
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                wish.executor = user
                wish.save()
                keyboard = get_friend_wishes_keyboard(user, wish.owner.id, wish.category, int(data[2]))
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['friend_wishes'],
                                                           {
                                                               "f_n": wish.owner.f_n,
                                                               "l_n": wish.owner.l_n,
                                                               "user_id": wish.owner.user_id,
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                               "executing": constants['executed'] if wish.executor
                                                               else constants['not_executed']
                                                           }), reply_markup=keyboard,
                                               action="edit_message", message_id=call.message.message_id)

        elif data[0] == "friend":
            if data[-1] == "list":
                await bot.add_message_to_queue(call.message.chat.id,
                                               text=format_text(messages_texts['friends_list']),
                                               action="edit_message", message_id=call.message.message_id,
                                               reply_markup=get_friends_keyboard(user, int(data[1])))
            elif data[-1] == "look":
                message, keyboard = get_friend_message_keyboard(user, data[1])
                await bot.add_message_to_queue(call.message.chat.id,
                                               text=message,
                                               action="edit_message", message_id=call.message.message_id,
                                               reply_markup=keyboard)
            elif data[-1] == "category":
                keyboard = get_friend_wishes_keyboard(user, data[1], data[2], int(data[3]))
                friend = UserModel.objects.get(id=data[1])
                if not keyboard:
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['friend_private'],
                                                               {
                                                                   "f_n": friend.f_n,
                                                                   "l_n": friend.l_n,
                                                                   "user_id": friend.user_id
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                else:
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['friend_wishes'],
                                                               {
                                                                   "f_n": friend.f_n,
                                                                   "l_n": friend.l_n,
                                                                   "user_id": friend.user_id,
                                                                   "wish_name": "",
                                                                   "wish_description": "",
                                                                   "executing": ""
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id,
                                                   reply_markup=keyboard)
            elif data[-1] == "wish":
                try:
                    wish = WishModel.objects.get(id=data[1])
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                keyboard = get_friend_wishes_keyboard(user, wish.owner.id, wish.category, int(data[2]))
                if not keyboard:
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['friend_private'],
                                                               {
                                                                   "f_n": wish.owner.f_n,
                                                                   "l_n": wish.owner.l_n,
                                                                   "user_id": wish.owner.user_id
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['friend_wishes'],
                                                           {
                                                               "f_n": wish.owner.f_n,
                                                               "l_n": wish.owner.l_n,
                                                               "user_id": wish.owner.user_id,
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                               "executing": constants['executed'] if wish.executor
                                                               else constants['not_executed']
                                                           }), reply_markup=keyboard,
                                               action="edit_message", message_id=call.message.message_id)
            elif data[-1] == "delete":
                friend = UserModel.objects.get(id=data[1])
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['friend_delete'],
                                                           {
                                                               "f_n": friend.f_n,
                                                               "l_n": friend.l_n,
                                                               "user_id": friend.user_id,
                                                           }),
                                               reply_markup=cancel_keyboard([
                                                   InlineKeyboardButton(text=constants['accept'],
                                                                        callback_data=f"friend:{data[1]}:delete_a")]),
                                               action="edit_message", message_id=call.message.message_id)
            elif data[-1] == "delete_a":
                friend = UserModel.objects.get(id=data[1])
                if friend in user.subscribes:
                    unsubscribe(user, friend)
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['friend_deleted'],
                                                               {
                                                                   "f_n": friend.f_n,
                                                                   "l_n": friend.l_n,
                                                                   "user_id": friend.user_id,
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id)
                else:
                    await bot.add_message_to_queue(call.message.chat.id,
                                                   format_text(messages_texts['friend_already_deleted'],
                                                               {
                                                                   "f_n": friend.f_n,
                                                                   "l_n": friend.l_n,
                                                                   "user_id": friend.user_id,
                                                               }),
                                                   action="edit_message", message_id=call.message.message_id)
        elif data[0] == "accepted":
            if data[-1] == "delete":
                try:
                    wish = WishModel.objects.get(id=data[1], executor=user, completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                wish.executor = None
                wish.save()
                keyboard = get_wishes_accepted_keyboard(user)
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['look_accepted_wishes'],
                                                           {
                                                               "wish_category": "",
                                                               "wish_name": "",
                                                               "wish_description": "",
                                                               "f_n": "",
                                                               "l_n": "",
                                                               "user_id": None
                                                           }), reply_markup=keyboard,
                                               action="edit_message", message_id=call.message.message_id)
            elif data[-1] == "look":
                try:
                    wish = WishModel.objects.get(id=data[1], executor=user, completed=False)
                except mongoengine.errors.DoesNotExist:
                    await bot.add_message_to_queue(call.message.chat.id, format_text(messages_texts['wish_expired']),
                                                   action="edit_message", message_id=call.message.message_id)
                    return
                keyboard = get_wishes_accepted_keyboard(user)
                await bot.add_message_to_queue(call.message.chat.id,
                                               format_text(messages_texts['look_accepted_wishes'],
                                                           {
                                                               "wish_category": format_text(wish.category),
                                                               "wish_name": wish.name,
                                                               "wish_description": wish.description,
                                                               "f_n": wish.owner.f_n,
                                                               "l_n": wish.owner.l_n,
                                                               "user_id": wish.owner.user_id
                                                           }), reply_markup=keyboard,
                                               action="edit_message", message_id=call.message.message_id)

    elif user.status['state'] == "add_wish":
        if data[-1] == "accept":
            wish = await save_wish(bot, user)
            await bot.add_message_to_queue(call.message.chat.id,
                                           text=format_text(messages_texts['saved_wish'],
                                                            {
                                                                "wish_name": wish.name,
                                                                "wish_category": format_text(wish.category),
                                                                "wish_description": wish.description
                                                            }),
                                           action="edit_message", message_id=call.message.message_id)