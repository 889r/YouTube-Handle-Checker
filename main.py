#main
import requests
import random
import string
import os
from telegram import Bot
import json
import asyncio

#logger / colorama
import logging
import colorama 
from colorama import Fore
from modules.logger import setup_logger

#----------------------------------------------------------

os.system("cls")
os.system("title Youtube Handle Checker  /  t.me/rei07x")


#colorama.initialise
colorama.init()

#setup logger
logger = setup_logger()


ascii_art = f""" 
                                              {Fore.CYAN}
                                              ╔═╗┬ ┬┌─┐┌─┐┬┌─┌─┐┬─┐
                                              ║  ├─┤├┤ │  ├┴┐├┤ ├┬┘
                                              ╚═╝┴ ┴└─┘└─┘┴ ┴└─┘┴└─
                                              {Fore.RESET}
"""

print(ascii_art)

def load_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

def check_youtube_handle(handle):
    url = f"https://www.youtube.com/@{handle}"
    response = requests.get(url)
    if response.status_code == 200:
        if "The channel you requested does not exist." in response.text:
            return "Available"  
        else:
            return "Taken"      
    elif response.status_code == 404:
        return "Available"   
    else:
        return None

def generate_random_handle(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

async def send_to_telegram(message, token, chat_id):
    try:
        if token and chat_id:  # Check if both token and chat_id are present
            bot = Bot(token=token)
            await bot.send_message(chat_id=chat_id, text=message)
    except asyncio.CancelledError:
        logger.warning("Coroutine cancelled while sending message to Telegram.")

async def main():
    config = load_config()
    length = int(input(f"                                   [{Fore.CYAN}?{Fore.RESET}] Length of usernames you want to check >>> "))
    os.system("cls")
    print()
    with open("valid.txt", "a", buffering=1) as valid_file:
        while True:
            try:
                name = generate_random_handle(length)
                availability = check_youtube_handle(name)
                if availability is None:
                    logger.error("An error occurred while checking the handle.")
                elif availability == "Available":
                    logger.info(f"The YouTube handle '{Fore.CYAN}{name}{Fore.RESET}' is {availability}.")
                    valid_file.write('@'+name + "<- Available Username / YouTube" '\n')  # Write available handle to valid.txt
                    await send_to_telegram(f"@{name} <- Available Username / YouTube", config.get("telegram_bot_token"), config.get("telegram_chat_id"))  # Use get() to handle absence of token or chat_id
            except KeyboardInterrupt:
                logger.info(f"[{Fore.LIGHTMAGENTA_EX}+{Fore.RESET}] Ctrl+C detected. Exiting....")
                break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
