from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup


reply_keyboard = [['/start', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start_command(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"""Привет {user.mention_html()}!""", reply_markup=markup
    )


async def user_message(update, context):
    with open('all_messages.txt', 'a', encoding='utf-8') as file:
        user = update.message.from_user.username
        text = update.message.text
        file.write(f"@{user}: {text}\n")


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... ")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, user_message)

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()