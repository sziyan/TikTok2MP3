#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import downloader as downloader_script
import os

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

try:
    token = os.environ.get('TOKEN')
except:
    print('TOKEN is not set!')


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Provide me with any TikTok URL and I will convert it to MP3 and send it back to you!')
    # user = update.effective_user
    # await update.message.reply_html(
    #     rf"Hi {user.mention_html()}!",
    #     reply_markup=ForceReply(selective=True),
    # )

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text
    if msg.startswith('https://vt.tiktok.com') or msg.startswith('https://www.tiktok.com'):
        await update.message.reply_text('Received your URL! Hold on while I convert to MP3...')
        try:
            download = downloader_script.download(msg)
            title = download[0]
            filename = download[1]
            await update.message.reply_text('{} converted successfully! \nHold on while I upload the file...'.format(title))
            await update.message.reply_audio(audio=open(filename, 'rb'))
            os.remove(filename)
            print('{} deleted from system.'.format(filename))
        except:
            await update.message.reply_text('An error occurred!')
    else:
        await update.message.reply_text('This is not a valid TikTok URL')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()