from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler, Application, MessageHandler, filters
from plot import MAP

BOT_TOKEN = "6292774773:AAHQnhCfZpJFNjJ5y9xFWaHpkII3f2HQ07c"

FIRST, SECOND = range(2)

ismagnet = False
iskeys = False



async def start_command(update, context):
    user = update.message.from_user.username
    await update.message.reply_html(f'Привет {user}! Нажми /start_game, чтобы создать пост.')
    return FIRST


async def game(update, context):
    keyboard = [[InlineKeyboardButton(MAP["спальня"]["actions"][0], callback_data='button_bathroom')],
                [InlineKeyboardButton(MAP["спальня"]["actions"][1], callback_data='button_kitchen')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    with open(MAP["спальня"]["img"], 'rb') as photo:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption=MAP["спальня"]["txt"],
                                     reply_markup=reply_markup)

    return FIRST


async def button(update, context):
    global ismagnet, iskeys
    user = update.callback_query.from_user.username
    query = update.callback_query

    if query:
        await query.answer()

    if query.message and query.data == 'button_bedroom':
        keyboard = [[InlineKeyboardButton(MAP["спальня"]["actions"][0], callback_data='button_bathroom')],
                    [InlineKeyboardButton(MAP["спальня"]["actions"][1], callback_data='button_kitchen')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["спальня"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["спальня"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_bathroom':
        keyboard = [[InlineKeyboardButton(MAP["ванная комната"]["actions"][0], callback_data='button_bedroom')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if ismagnet:
            with open(MAP["ванная комната"]["img"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo,
                                             caption=MAP["ванная комната"]["txt_magnit"], reply_markup=reply_markup)
                iskeys = True
        elif iskeys:
            with open(MAP["ванная комната"]["img"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo,
                                             caption=MAP["ванная комната"]["txt_iskeys"], reply_markup=reply_markup)
        else:
            with open(MAP["ванная комната"]["img"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo,
                                             caption=MAP["ванная комната"]["txt"], reply_markup=reply_markup)

    if query.message and query.data == 'button_kitchen':
        keyboard = [[InlineKeyboardButton(MAP["кухня"]["actions"][0], callback_data='button_bedroom')],
                    [InlineKeyboardButton(MAP["кухня"]["actions"][1], callback_data='button_entrance')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if ismagnet:
            with open(MAP["кухня"]["img"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["кухня"]["txt_has_magnet"],
                                             reply_markup=reply_markup)
        else:
            with open(MAP["кухня"]["img"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["кухня"]["txt"],
                                             reply_markup=reply_markup)
                ismagnet = True
    if iskeys:
        if query.message and query.data == 'button_entrance':
            keyboard = [[InlineKeyboardButton(MAP["подъезд"]["actions"][0], callback_data='button_entrance_up')],
                        [InlineKeyboardButton(MAP["подъезд"]["actions"][1], callback_data='button_entrance_down')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            with open(MAP["подъезд"]["img"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["подъезд"]["txt"],
                                             reply_markup=reply_markup)
    else:
        if query.message and query.data == 'button_entrance':
            keyboard = [[InlineKeyboardButton(MAP["кухня"]["actions"][0], callback_data='button_bedroom')],
                        [InlineKeyboardButton(MAP["кухня"]["actions"][1], callback_data='button_entrance')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            with open(MAP["подъезд"]["img_nokeys"], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["подъезд"]["txt_nokeys"],
                                             reply_markup=reply_markup)


    if query.message and query.data == 'button_entrance_up':
        keyboard = [[InlineKeyboardButton(MAP["наверх"]["actions"][0], callback_data='button_red')],
                    [InlineKeyboardButton(MAP["наверх"]["actions"][1], callback_data='button_blue')],
                    [InlineKeyboardButton(MAP["наверх"]["actions"][2], callback_data='button_green')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["наверх"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["наверх"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_entrance_down':
        keyboard = [[InlineKeyboardButton(MAP["вниз"]["actions"][0], callback_data='button_red')],
                    [InlineKeyboardButton(MAP["вниз"]["actions"][1], callback_data='button_blue')],
                    [InlineKeyboardButton(MAP["вниз"]["actions"][2], callback_data='button_green')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["вниз"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["вниз"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_red':
        keyboard = [[InlineKeyboardButton(MAP["красный"]["actions"][0], callback_data='button_green')],
                    [InlineKeyboardButton(MAP["красный"]["actions"][1], callback_data='button_blue')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["красный"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["красный"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_blue':
        keyboard = [[InlineKeyboardButton(MAP["синий"]["actions"][0], callback_data='button_green')],
                    [InlineKeyboardButton(MAP["синий"]["actions"][1], callback_data='button_red')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["синий"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["синий"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_green':
        keyboard = [[InlineKeyboardButton(MAP["зеленый"]["actions"][0], callback_data='button_outside')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["зеленый"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["зеленый"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_outside':
        keyboard = [[InlineKeyboardButton(MAP["На улицу"]["actions"][0], callback_data='button_coffee')],
                    [InlineKeyboardButton(MAP["На улицу"]["actions"][1], callback_data='button_diksi')],
                    [InlineKeyboardButton(MAP["На улицу"]["actions"][2], callback_data='button_shaverma')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["На улицу"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["На улицу"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_coffee':
        keyboard = [[InlineKeyboardButton('Пройти снова', callback_data='button_bedroom')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["кафе"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["кафе"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_diksi':
        keyboard = [[InlineKeyboardButton('Пройти снова', callback_data='button_bedroom')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["дикси"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["дикси"]["txt"],
                                         reply_markup=reply_markup)

    if query.message and query.data == 'button_shaverma':
        keyboard = [[InlineKeyboardButton('Пройти снова', callback_data='button_bedroom')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(MAP["шаверма"]["img"], 'rb') as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=MAP["шаверма"]["txt"],
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
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
