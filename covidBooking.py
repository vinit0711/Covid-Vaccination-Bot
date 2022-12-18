#!/usr/bin/env python
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from datetime import datetime, timedelta

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
FIRSTNAME, LASTNAME,  LOCATION, CATEGORY_HANDLING, BIO, DATE, SLOT = range(8)

user_details = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hi! Welcome to Covid Vaccination Booking System.\n"
        "Please Enter Your First Name ",
    )
    return FIRSTNAME


async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_details.update({"first_name": update.message.text})
    logger.info("FIRSTNAME of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        f"Please Enter your Last Name",
        reply_markup=ReplyKeyboardRemove()
    )
    return LASTNAME


async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_details.update({"last_name": update.message.text})
    logger.info("LASTNAME  %s  ", update.message.text)
    await update.message.reply_text(
        "Please enter You location . ",
        reply_markup=ReplyKeyboardRemove()
    )
    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_location = update.message.text
    user_details.update({"location": update.message.text})
    logger.info(f"Location of {user.first_name} : {user_location}")
    keyboard = [
        [
            InlineKeyboardButton("1st Dose", callback_data="1st Dose"),
            InlineKeyboardButton("2nd Dose ", callback_data="2nd Dose"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose a Category", reply_markup=reply_markup)
    return CATEGORY_HANDLING



async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    query = update.callback_query
    category_selected_data = query.data
    user_details.update({"category": category_selected_data})
    dates = [(datetime.today() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, 4)]

    keyboard = [
        [
            InlineKeyboardButton(dates[0], callback_data=dates[0]),
            InlineKeyboardButton(dates[1], callback_data=dates[1]),
            InlineKeyboardButton(dates[2], callback_data=dates[2]),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please choose a Date", reply_markup=reply_markup)
    return DATE


async def date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    query = update.callback_query
    date_selected = query.data
    user_details.update({"Date": date_selected})
    keyboard = [
        [
            InlineKeyboardButton("10am -12pm", callback_data="10am -12pm"),
            InlineKeyboardButton("12pm - 2pm", callback_data="12pm - 2pm"),
            InlineKeyboardButton("2pm - 4pm", callback_data="2pm - 4pm"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please Select Slot For Selected Date", reply_markup=reply_markup)
    return SLOT

async def slot_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    query = update.callback_query
    slot_selected = query.data
    user_details.update({"Slot": slot_selected})

    await query.edit_message_text(
        f'Your COVID Vaccination Booking Is Confirmed. '
        f' \n Name : {user_details["first_name"]} {user_details["last_name"]}'
        f'\n Location : {user_details["location"]}'
        f'\n Category : {user_details["category"]}'
        f'\n Date : {user_details["Date"]}'
        f'\n Slot  : {user_details["Slot"]}  ')
    return ConversationHandler.END




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:

    application = Application.builder().token("5624641945:AAE5HPOqJfdFtkelQmGrFtgd5cXOeMxh_Cc").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(["book","Book"], start)],
        states={
            FIRSTNAME: [MessageHandler(filters.TEXT, first_name)],
            LASTNAME: [MessageHandler(filters.TEXT, last_name)],
            LOCATION: [MessageHandler(filters.TEXT, location)],
            CATEGORY_HANDLING: [CallbackQueryHandler(category)],
            DATE: [CallbackQueryHandler(date_selection)],
            SLOT: [CallbackQueryHandler(slot_selection)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
