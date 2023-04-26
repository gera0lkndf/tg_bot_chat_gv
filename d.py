from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Application, MessageHandler, filters
from config import BOT_TOKEN


# BOT_TOKEN = "6292774773:AAHQnhCfZpJFNjJ5y9xFWaHpkII3f2HQ07c"

reply_keyboard = [['/start_game'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


FIRST, SECOND = range(2)


async def start_command(update, context):
    user = update.message.from_user.username
    await update.message.reply_html(f'Привет {user}! Нажми /start_game, чтобы создать пост.', reply_markup=markup)
    return FIRST


async def help_command(update, context):
    user = update.message.from_user.username
    keyboard = [[InlineKeyboardButton("start", callback_data='a'),
                 InlineKeyboardButton("stop", callback_data='b')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Привет {user}!", reply_markup=reply_markup)


async def game(update, context):
    keyboard = [[InlineKeyboardButton("Выйти в левый коридор", callback_data='button1'),
                 InlineKeyboardButton("Изучить дверь", callback_data='button2'),
                 InlineKeyboardButton("Выйти в правый коридор", callback_data='button3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open('img.png', 'rb') as photo:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption='Текст поста',
                                     reply_markup=reply_markup)

    return FIRST


async def button(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("Выйти в левый коридор", callback_data='button1'),
                 InlineKeyboardButton("Изучить дверь", callback_data='button2'),
                 InlineKeyboardButton("Выйти в правый коридор", callback_data='button3')]]
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
            FIRST: [CommandHandler('start_game', game)],
            SECOND: []
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    text_handler = MessageHandler(filters.TEXT, user_message)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()