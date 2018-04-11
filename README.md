# python-telegram-bot

This started off as a echo bot, but as it figures out that the function is the heart of everything and this is where we can make the most happen.

For now, it is storing all the chats in a file.

def echo(bot, update):
    """Echo the user message."""
    print(update.message.text)
    allMessages.append(update.message.text)
    print(type(update.message.text))
    writeLineToFile(file,update.message.text)
    update.message.reply_text(update.message.text)


