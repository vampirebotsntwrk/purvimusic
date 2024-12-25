



from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    ABUTTON = [[InlineKeyboardButton("˹ sᴜᴘᴘᴏꝛᴛ ˼", url="https://t.me/https://t.me/+E8x1hf2jWBQ0ZDg1")],[InlineKeyboardButton("˹ ᴜᴘᴅᴧᴛᴇ ˼", url="https://t.me/THUNDERDEVS"),
    InlineKeyboardButton("˹ ᴧʟʟ ʙᴏᴛ ˼", url="https://t.me/ll_MY_BOTS")],[InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data=f"settingsback_helper"),
    ]]

    UBUTTON = [[InlineKeyboardButton("˹ ᴍᴜsɪᴄ ˼", callback_data="settings_back_helper"),InlineKeyboardButton("˹ ᴛᴏᴏʟs ˼", callback_data=f"mbot_cb")],[InlineKeyboardButton("˹ ᴍᴧɴᴧɢᴇ ˼", callback_data=f"bbot_cb"),
    InlineKeyboardButton("˹ ʀᴧɪᴅ ˼", callback_data="cplus HELP_raid")],[InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data=f"settingsback_helper"),
    ]]
