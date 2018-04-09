from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from sys import argv


def print_options(list_task):
    string = ''
    for (i, item) in list_task.items():
        string += str(item) + '\n'
    return string


def remove_item(list_task, item):
    for element in list_task:
        element = element.split()
        if item in element:
            element = ' '.join(element)
            list_task.remove(element)


def start(bot, update):
    options = {
        1: "/showTasks",
        2: "/newTask",
        3: "/removeTask",
        4: "/removeAllTasks"
    }

    bot.send_message(chat_id=update.message.chat_id, text=print_options(options))


def error_text(bot, update):
    # simulate typing from the bot
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

    # send the error message
    update.message.reply_text("I'm sorry. I can't do that.")


def show_tasks(bot, update):
    if len(tasks) == 0:
        update.message.reply_text("Nothing to do, here!")
    else:
        update.message.reply_text(tasks)


def new_task(bot, update, args):
    tasks.append(' '.join(args))
    update.message.reply_text("Task successfully added.")


def remove_task(bot, update, args):
    try:
        task = ' '.join(args)
        tasks.remove(task)
        update.message.reply_text("The task was successfully deleted.")
    except ValueError:
        update.message.reply_text("The task you specified is not in the list.")


def remove_all(bot, update):
    if len(tasks) == 0:
        print("I didn't find any task to delete!")
    else:
        tasks.clear()
        update.message.reply_text("Tasks successfully deleted.")


def main():

    updater = Updater('Code API')

    # dispatcher
    dp = updater.dispatcher

    # add the command handler commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", show_tasks))
    dp.add_handler(CommandHandler("newTask", new_task, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", remove_task, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", remove_all))

    dp.add_handler(MessageHandler(Filters.text, error_text))

    # start the bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    filename = argv[1]
    txt = open(filename)  # open the file

    file_tasks = txt.read()  # reading the file
    tasks = file_tasks.split('\n')
    txt.close()

    main()