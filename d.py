from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Application
from config import BOT_TOKEN


reply_keyboard = [['/post', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


FIRST, SECOND = range(2)


async def start_command(update, context):
    user = update.message.from_user.username
    await update.message.reply_html(f'Привет {user}! Нажми /post, чтобы создать пост.', reply_markup=markup)
    return FIRST


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... ")


async def post(update, context):
    keyboard = [[InlineKeyboardButton("Кнопка 1", callback_data='button1'),
                 InlineKeyboardButton("Кнопка 2", callback_data='button2'),
                 InlineKeyboardButton("Кнопка 3", callback_data='button3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open('photo.jpg', 'rb') as photo:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption='Текст поста',
                                     reply_markup=reply_markup)

    return FIRST


async def button(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton("Кнопка 1", callback_data='button1'),
                 InlineKeyboardButton("Кнопка 2", callback_data='button2'),
                 InlineKeyboardButton("Кнопка 3", callback_data='button3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == 'button1':
        with open('photo2.jpg', 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption='Другой текст',
                                         reply_markup=reply_markup)

    return FIRST


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            FIRST: [CommandHandler('post', post)],
            SECOND: []
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
    application.idle()


if __name__ == '__main__':
    main()