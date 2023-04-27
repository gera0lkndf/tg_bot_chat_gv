from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Application, MessageHandler, filters

BOT_TOKEN = "6292774773:AAHQnhCfZpJFNjJ5y9xFWaHpkII3f2HQ07c"

FIRST, SECOND = range(2)

users = {}


async def start_command(update, context):
    user = update.message.from_user.username
    users[user] = "спальня"
    await update.message.reply_html(f'Привет {user}! Нажми /start_game, чтобы создать пост.')
    return FIRST


async def help_command(update, context):
    user = update.message.from_user.username
    await update.message.reply_text(f"Привет {user}!")
    keyboard = [[InlineKeyboardButton("start", callback_data='a'),
                 InlineKeyboardButton("stop", callback_data='b')]]
    reply_markup = InlineKeyboardMarkup(keyboard)


async def game(update, context):
    keyboard = [[InlineKeyboardButton("Выйти в правый корридор", callback_data='button1')],
                [InlineKeyboardButton("Зайти в левый корридор", callback_data='button2')],
                [InlineKeyboardButton("Изучить дверь", callback_data='button3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open('img.png', 'rb') as photo:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption='Текст поста',
                                     reply_markup=reply_markup)

    return FIRST


async def button(update, context):
    user = update.message.from_user.username
    query = update.callback_query
    print(query)
    if query:
        await query.answer()
        users[user] = query.data

    keyboard = [[InlineKeyboardButton("Выйти в правый корридор", callback_data='button1')],
                [InlineKeyboardButton("Выйти в левый корридор", callback_data='button2')],
                [InlineKeyboardButton("Изучить дверь", callback_data='button3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == 'button1':
        with open('img1.jpg', 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption='первый вариант',
                                         reply_markup=reply_markup)
    if query.data == 'button2':
        with open('img2.jpg', 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption='второй вариант',
                                         reply_markup=reply_markup)
    if query.data == 'button3':
        with open('img3.jpg', 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption='третий вариант',
                                         reply_markup=reply_markup)

    return FIRST


async def user_message(update, context):
    with open('all_messages.txt', 'a', encoding='utf-8') as file:
        user = update.message.from_user.username
        text = update.message.text
        file.write(f"@{user}: {text}\n")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            FIRST: [CommandHandler('start_game', button)],
            SECOND: []
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    text_handler = MessageHandler(filters.TEXT, user_message)
    application.add_handler(CommandHandler("start", start_command))
    # application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(text_handler)
    application.run_polling()
    application.idle()


if __name__ == '__main__':
    main()
