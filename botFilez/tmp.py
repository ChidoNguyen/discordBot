import multiprocessing , subprocess
from testbot import run_bot
from bookAPI import start_app


def main():
    bot_process = multiprocessing.Process(target=run_bot)
    api_process = multiprocessing.Process(target=start_app)
    bot_process.start()
    api_process.start()
    bot_process.join()
    api_process.terminate()
    api_process.join()
    return

if __name__ == '__main__':
   main()