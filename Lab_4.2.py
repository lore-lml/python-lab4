from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import ChatAction
import mysql.connector

updater = Updater("598486728:AAHxLy96_9grf-0qx7Kfmnjr06I8d8-XnmA")
dp = updater.dispatcher

conn = mysql.connector.connect(user='root', password='asdf12345', host='localhost', database='tasks')


def start(bot,update):
    update.message.reply_text("This is your tasks_bot!")


def showTasks(bot, update):
    query = "SELECT todo FROM task_list ORDER BY todo ASC"
    cursor = conn.cursor()
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    cursor.execute(query)
    result = cursor.fetchall()
    length = len(result)
    if length == 0:
        update.message.reply_text("Nothing to do!")
    #result.sort()
    i = 0
    text = ""
    while i < length:
        text += "- "+result[i][0]
        if i < length-1:
            text += "\n"
        i += 1
    update.message.reply_text(text)
    cursor.close()


def newTask(bot, update, args):
    text = ""
    i = 0
    while i < len(args):
        text += args[i]
        if i < len(args) - 1:
            text += " "
        i += 1
    query = "INSERT into task_list (todo) VALUES (%s)"
    cursor = conn.cursor()
    cursor.execute(query, (text,))
    conn.commit()
    update.message.reply_text("Task has been added succesfully!")
    cursor.close()

def removeTask(bot, update, args):
    text = ""
    i=0
    while i < len(args):
        text += args[i]
        if i < len(args)-1:
            text += " "
        i += 1
    query = "SELECT id FROM task_list WHERE todo=%s"
    cursor = conn.cursor()
    cursor.execute(query, (text,))
    result = cursor.fetchone()
    """if len(result) != 0:
        print(result)
        print(result[0])"""

    if result == None:
        update.message.reply_text("None task has that name!")
        cursor.close()
        return
    id = result[0]
    query = "DELETE FROM task_list WHERE id=%s"
    cursor.execute(query, (id,))
    conn.commit()
    update.message.reply_text("Task has been removed successfully!")
    cursor.close()

def removeAllTasks(bot, update):
    cursor = conn.cursor()
    query = "TRUNCATE TABLE task_list"
    cursor.execute(query)
    conn.commit()
    update.message.reply_text("Every task has been removed!")
    cursor.close()

def unknown(bot, update):
    update.message.reply_text("Unrecognized command!")


if __name__ == "__main__":
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("show_tasks", showTasks))
    dp.add_handler(CommandHandler("new_task", newTask, pass_args=True))
    dp.add_handler(CommandHandler("remove_task", removeTask, pass_args=True))
    dp.add_handler(CommandHandler("remove_all_tasks", removeAllTasks))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()
    conn.close()
