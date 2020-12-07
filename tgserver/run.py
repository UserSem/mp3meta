from telegram.update import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

import config
import db

updater = Updater(token=config.TOKEN, use_context=True)
dispatcher = updater.dispatcher


def addme(group: str, update: Update, context: CallbackContext):
    err = db.add_user(update.effective_user)
    if err:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error adding user ({err})")
        return
    admins = db.add_request(group, update.effective_user.id)
    for admin_id in admins:
        context.bot.send_message(
            chat_id=admin_id,
            text=f"User [{update.effective_user.id}] "
                 f"{update.effective_user.first_name} "
                 f"{update.effective_user.username} {update.effective_user.last_name} "
                 f"requested access to {group}!"
        )


def process(update: Update, context: CallbackContext):
    try:
        command = update.message.text.split()
        if command[0].lower() == 'addme':
            if len(command) == 2:
                addme(command[1], update, context)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Command: addme <group>")
        elif command[0].lower() == 'myid':
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Your ID is {str(update.effective_chat.id)}")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown message!")
    except Exception as exc:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Unknown error ({exc})")


echo_handler = MessageHandler(Filters.all, callback=process)
dispatcher.add_handler(echo_handler)
updater.start_polling()
