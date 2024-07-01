<h1 align="center">Discord Book Bot</h1>
---
# Features
- Bot:
  - !getbook (main feature) : "!getbook author title" Bot will provide attached file of requested publication.
  - !tellmeajoke : Will in the future tell some funny jokes.
  - !shutdown : Restricted to owner/admin; will shut the bot down, if ran concurrently with Flask API server will also be shutdown.
  - !help : Gets you the above info.
- Flask API:
  - Allows for Bot to make GET/POST requests to initiate different actions. Created to decouple the Bot's need to handle subprocesses.
  - Depending on which request is sent in; API will spin up subprocess to execute Selenium script, and do clean up afterwards.
- Selenium Automation:
  - Automatically login, navigate, and download on specified webpage.
  - Utilizes different aspect of HTML/CSS components to hopefully make it more robust to site upgrades. 
---
# Tools and Technologies Used
- **Python** : Primary programming language used for all components of the project.
- **Flask** : Used to create an API endpoint web server, allowing for the Bot to interact with it via HTTP requests.
- **Discord.py** : A Python wrapper for the Discord API, used to create the Discord Bot.
- **Selenium** : Browser automation to navigate, locate, and download requested publications.
- **Requests** : Used for making HTTP requests to API endpoint by the Discord Bot.
- **Multiprocessing** : Used to manage multiple processed, coupled the initiation and shutdown of Bot + API. 
- **HTML/CSS** : Used in conjunction with Selenium to locate web elements.
---
# Installation/Requirements
- Python
- Discord
- discordCreds.py required attributes :
  1. myDiscordCreds = 'YOUR OWN BOT TOKEN' (str)
  2. siteURL = (str) Bot works only for 1 specific site.
  3. userID = (str) User ID for site.
  4. userPASS = (str) User Password for site.
  5. desired_saved_dir = (str) Directory you want to save your downloads in.
  6. adminID = (int) Your own Discord ID number to restrict access to other users.
- pip install requirements.txt
