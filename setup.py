#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# setup.py
# author: xdavidhu

from telegram.ext import Updater, MessageHandler, Filters
from random import randint
import telegram
import json
import os

if __name__ == '__main__':
    GREEN = '\033[1m' + '\033[32m'
    WHITE = '\033[1m' + '\33[97m'
    END = '\033[0m'
    header = """
                    """ + GREEN + """ _            """ + WHITE + """  _____ _               _     .-.
                    """ + GREEN + """| |           """ + WHITE + """ / ____| |             | |   | OO|
                    """ + GREEN + """| | __ _ _ __ """ + WHITE + """| |  __| |__   ___  ___| |_  |   |
                    """ + GREEN + """| |/ _` | '_ \\""" + WHITE + """| | |_ | '_ \ / _ \/ __| __| '^^^'
                    """ + GREEN + """| | (_| | | | """ + WHITE + """| |__| | | | | (_) \__ | |_
                    """ + GREEN + """|_|\__,_|_| |_""" + WHITE + """|\_____|_| |_|\___/|___/\__|
                    """
    try:
        print(header + """          v1.0 """ + WHITE + """by David Schütz (@xdavidhu)    """ + "\n" + END)
    except:
        print(header + """                         v1.0 """ + WHITE + """by @xdavidhu    """ + "\n" + END)

    print("[I] Step 1 / 3:\n")
    interface = input("[?] Please enter the name of the network interface " +\
                        "connected/will be connected to the target LAN: ")
    print("[+] Interface '" + interface + "' set.")
    os.system("clear")
    print("\n\n[I] Step 2 / 3:\n")
    print("[+] Please create a Telegram API key by messaging @BotFather on " +\
            "Telegram with the command '/newbot'.\n\nAfter this, @BotFather "+\
            "will ask you to choose a name for your bot. This can be "+\
            "anything you want.\n\nLastly, @BotFather will ask you for a "+\
            "username for your bot. You have to choose a unique username "+\
            "here which ends with 'bot'. For example: xdavidbot. Make note "+\
            "of this username, since later you will have to search for this "+\
            "to find your bot, which lanGhost will be running on.\n\nAfter "+\
            "you send you username of choise to @BotFather, you will "+\
            "recieve your API key. Please enter it here:\n")
    telegram_api = input("[?] Telegram API key: ")
    os.system("clear")
    print("\n\n[I] Step 3 / 3:\n")
    print("[+] Now for lanGhost to only allow access to you, you need to "+\
            "verify yourself.\n\nSend the verification code below TO THE BOT"+\
            " you just created. Just search for your bot's @username "+\
            "(what you sent to @BotFather) to find it.")
    verification_code = ''.join(str(randint(0,9)) for _ in range(6))
    print("\n[+] Verification code to send: " + verification_code)
    admin_chatid = False
    def check_code(bot, update):
        global admin_chatid
        if update.message.text == verification_code:
            bot.send_message(chat_id=update.message.chat_id, text="✅ Verification successful.")
            admin_chatid = str(update.message.chat_id)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="❌ Incorrect code.")

    try:
        updater = Updater(token=telegram_api)
    except:
        print("[!] Telegram API token is invalid... Please try again.")
    dispatcher = updater.dispatcher

    verify_handler = MessageHandler(Filters.text, check_code)
    dispatcher.add_handler(verify_handler)

    print("\n[+] Waiting for your message...")
    updater.start_polling()

    while True:
        try:
            if not admin_chatid == False:
                print("\n[+] Device linked successfully! Shutting down the "+\
                        "temporary Telegram bot, please wait a second...")
                updater.stop()
                break
        except:
            print("\n[!] Failed to get your chat ID, please try again. Exiting...")
            updater.stop()
            exit()

    print("[+] Generating config file...")
    config_object = {"interface": interface, "telegram_api": telegram_api, "admin_chatid": admin_chatid}
    config_json = json.dumps(config_object)
    script_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    with open(script_path + "config.cfg", "w") as f:
        f.write(config_json)
        f.close()
    print("[+] Setup done.")
