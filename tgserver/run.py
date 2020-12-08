import os.path

from telegram.update import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

import config
import db

import sys
sys.path.append(os.path.abspath('../..'))
from mp3meta import main

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
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        def reply_to_chat(text: str):
            context.bot.send_message(chat_id, text)
        command = ['']
        if update.message.text:
            command = update.message.text.split()
        if command[0].lower() == 'addme':
            if len(command) == 2:
                addme(command[1], update, context)
            else:
                reply_to_chat("Command: addme <group>")
        elif command[0].lower() == 'myid':
            reply_to_chat(f"Your ID is {user_id}")
        elif command[0].lower() == 'adduser':
            user_id, group_name = command[1], command[2]
            sender_id = update.effective_user.id
            err = db.add_user_to_group(user_id, group_name, sender_id)
            if err:
                reply_to_chat(err)
            else:
                reply_to_chat(f"User {user_id} added to group {group_name}")
                context.bot.send_message(chat_id=user_id,
                                         text=f"You were added to group {group_name}")
        elif command[0].lower() == 'find':
            if len(command) < 3:
                reply_to_chat("Command: find <group> <name/tag>")
                return
            files = db.search_files(command[2:], command[1])
            reply_to_chat(f"Results: {files}")



        elif update.message.audio:
            reply_to_chat(f"Got an audio!\n "
                          f"Name: {update.message.audio.file_name}")
            if not update.message.audio.file_name.endswith(".mp3"):
                reply_to_chat(f"Not an mp3 file! {update.message.audio.file_name}")
                return
            group_name = update.message.text
            if not group_name:
                group_name = db.get_user_groups(update.effective_user.id)
                if len(group_name) != 1:
                    reply_to_chat("Specify your group!")
                    return
                group_name = group_name[0]
            else:
                if group_name not in db.get_user_groups(update.effective_user.id):
                    reply_to_chat("Invalid group!")
                    return
            file_to_download = update.message.audio.get_file()
            file_name = update.message.audio.file_name
            file_path = os.path.join(config.MUSIC_FOLDER, file_name)
            file_to_download.download(file_path)
            mp3_file = main.Mp3File(file_path)
            tags = mp3_file.get_tags()
            tag_out = '\n'.join(f"{tag}: {' - ' if not val else val}" for tag, val in tags.items())
            reply_to_chat(f"Got tags: \n{tag_out}")
            db.add_file_to_db(file_name, group_name)
            db.set_current_file(user_id, file_name)
            db.write_tags_to_db(file_name, tags)

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown message!")
    except Exception as exc:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Unknown error ({exc})")


echo_handler = MessageHandler(Filters.all, callback=process)
dispatcher.add_handler(echo_handler)
updater.start_polling()
