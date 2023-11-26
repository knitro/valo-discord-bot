# valo-discord-bot

A discord bot originally developed to learn more about python and experiment the discord.py library.

## Prerequisites

- python3
- pip install discord.py
- pip install firebase_admin

## Current Functionality

### valo_news.py

- Simple bot that generates the patch notes link of whatever the user specifies. Otherwise it returns the latest patch.
- _Note: the latest patch is currently hardcoded. Will need to integrate with Riot API or use alternative methods to retrieve this information._

### valups_bot.py

- Discord bot to support lineup generation for **Valups**.
- Makes it easy to generate data that can be imported into **Valups** through a CSV file or by copy pasting the data straight into the WebApp in edit mode (edit
  mode TBD).
