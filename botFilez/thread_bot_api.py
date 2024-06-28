import threading

from bookAPI import app as book_API
from discordBot import run_discord_bot as discord_bot


def run_discord_bot():
    discord_bot()

def run_book_api():
    book_API.run(host='127.0.0.1' , port=5000)

if __name__ == "__main__":
    print("Bot started.")
    api_thread = threading.Thread(target=run_book_api)
    bot_thread = threading.Thread(target=run_discord_bot)

    bot_thread.start()
    api_thread.start()

    bot_thread.join()
    api_thread.join()
    print("Bot terminated along with threads")



