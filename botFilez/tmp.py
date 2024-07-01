import multiprocessing
from testbot import run
from bookAPI import spin_up

def main():
    bot_process = multiprocessing.Process(target=run)
    api_process = multiprocessing.Process(target=spin_up)
    bot_process.start()
    api_process.start()
    bot_process.join()
    api_process.terminate()
    api_process.join()
    return

if __name__ == '__main__':
    main()