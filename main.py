import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Replace with your actual Telegram bot token
BOT_TOKEN = os.getenv('BOT_TOKEN', '7819424071:AAF_5CKNCnnFkI7fLNdWsoNM1KzhoGQ_ewY')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("About", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 👋",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
🤖 <b>Bot Commands:</b>
/start - Start the bot
/help - Show this help message
/about - About this bot
/echo <text> - Echo back your text

🛠 <b>Features:</b>
- Inline buttons
- Echo messages
- Simple interaction
"""
    await update.message.reply_html(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send information about the bot."""
    about_text = """
🔹 <b>Render Telegram Bot</b> 🔹

This is a simple Telegram bot deployed on Render.com.

<b>Features:</b>
- Python 3.10+
- python-telegram-bot v20+
- Webhook setup
- Ready for Render deployment
"""
    await update.message.reply_html(about_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await help_command(update, context)
    elif query.data == 'about':
        await about_command(update, context)

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("echo", echo))
    
    # Add button handler
    application.add_handler(CallbackQueryHandler(button))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot in webhook mode for Render
    port = int(os.environ.get('PORT', 8443))
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if webhook_url:
        # Production (Render)
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{webhook_url}/{BOT_TOKEN}"
        )
    else:
        # Development (polling)
        application.run_polling()

if __name__ == "__main__":
    main()
