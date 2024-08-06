from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace 'YOUR_TOKEN' with the token provided by BotFather
TOKEN = 'YOUR_TOKEN'
BASE_REFERRAL_URL = 'https://webapp.bizex.io'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract the 'ref' parameter from the deep link (if provided)
        args = context.args  # context.args contains the list of arguments passed after the command
        ref = args[0] if args else ''
        
        # Create a referral URL using the 'ref' parameter
        referral_url = f"{BASE_REFERRAL_URL}?refare={ref}"
        
        # Create a button with the referral URL
        keyboard = [[InlineKeyboardButton("Visit Website", url=referral_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send a message with the button
        await update.message.reply_text('Click the button below to visit the website:', reply_markup=reply_markup)
    except Exception as e:
        print(f"Error in start handler: {e}")
        await context.application.shutdown()  # Shutdown the application on error

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        
        # Extract the dynamic part from the callback data
        ref = query.data
        
        # Create a referral URL using the dynamic part
        referral_url = f"{BASE_REFERRAL_URL}?ref={ref}"
        
        # Create a button with the referral URL
        keyboard = [[InlineKeyboardButton("Visit Website", url=referral_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message with the new button
        await query.edit_message_text(text="Click the button below to visit the website:", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error in button handler: {e}")
        await context.application.shutdown()  # Shutdown the application on error

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and shutdown the bot."""
    print(f"An error occurred: {context.error}")
    await context.application.shutdown()  # Shutdown the application on error

def main():
    # Set up the application
    application = Application.builder().token(TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Register the error handler
    application.add_error_handler(error_handler)

    # Start polling for updates from Telegram
    application.run_polling()

if __name__ == '__main__':
    main()
