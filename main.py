import asyncio
import logging
import signal
import sys
import traceback
from time import sleep
import telebot.async_telebot
from configs.telegram_api import config as tg_api
from modules.callback_coordinator import callback_coordinator
from modules.contact_coordinator import contact_coordinator
from modules.message_coordinator import message_coordinator
from modules.commands_coordinator import command_coordinator
from modules.setup_logger import special_logger, setup_logger
from modules.telegram_bot import TgBot
from configs.commands import config as commands_config



class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        logging.error(f"{traceback.format_exc()}")
        return True


bot = TgBot(token=tg_api['telegram_bot_token'], exception_handler=ExceptionHandler())



@bot.message_handler(commands=list(commands_config['default'].keys()))
async def commands(message: telebot.types.Message):
    if await bot.check_rules(message):
        await command_coordinator(bot, message)

@bot.message_handler(func=lambda message: True, content_types=["contact"])
async def contacts(message):
    if await bot.check_rules(message):
        await contact_coordinator(bot, message)


@bot.message_handler(func=lambda message: True)
async def any_message(message):
    if await bot.check_rules(message):
        await message_coordinator(bot, message)

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call: telebot.types.CallbackQuery):
    if await bot.check_rules(callback=call):
        await callback_coordinator(bot, call)


async def main():
    main_flag = True

    exceptions_logger = special_logger("exceptions", logging.FATAL, to_console=True)

    while main_flag:
        from configs.bot_settings import config as bot_settings
        main_flag = bot_settings['work']

        try:
            await asyncio.gather(bot.daemons_work(), bot.infinity_polling(timeout=90))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except telebot.async_telebot.asyncio_helper.RequestTimeout:
            exceptions_logger.fatal(f"{traceback.format_exc()}")
            sleep(60)
        except Exception:
            exceptions_logger.fatal(f"{traceback.format_exc()}")
            logging.error(f"{traceback.format_exc()}")
            sleep(20)

setup_logger()
logging.info("APP START")


try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(
        bot.set_my_commands([telebot.types.BotCommand(command, description)
                             for command, description in commands_config['default'].items()],
                            language_code='ru'))
    sys.exit(asyncio.run(main()))
except KeyboardInterrupt:
    logging.info(f"APP STOPPED")
except Exception:
    logging.error(f"{traceback.format_exc()}")


def end_read(*args):
    logging.info(f"APP STOPPED")

signal.signal(signal.SIGINT, end_read)
