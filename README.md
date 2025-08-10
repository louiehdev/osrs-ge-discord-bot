# Old School Runescape Grand Exchange Price Checker Bot

A discord bot that parses up to date information about items from the OSRS Wiki and pricing API's and formats it in an easy to read message embed. The bot is able to find items with multiple versions, such as poisoned weapons, as well as give recommendations if the specific item is not found. 

## Installation
```Python
git clone <repository_url>
cd <repository_directory>
```

## Install Dependencies
```Python
pip install discord.py
pip install requests
pip install dotenv
```

## Usage and Examples
When the bot is running, type in '$price' followed by the item you want to get the price information for.

<img width="479" height="382" alt="osrsgebotexample1" src="https://github.com/user-attachments/assets/56335267-a124-45dd-ac23-9bf757635e4a" />

If the item has multiple versions, the bot will ask you to clarify which version you are looking for. Respond with the appropriate number.

<img width="866" height="507" alt="osrsgebotexample2" src="https://github.com/user-attachments/assets/a1fb77de-0913-4c16-acde-d856169affc1" />

## Additional Instructions
I don't have the capability to keep this bot running at all times. If you would like to run it yourself, make sure to create a [Discord Developer Profile](https://discord.com/developers/) and create your own app. This allows you to get a Discord Bot Token which you will need to plug into the code (I suggest adding it into a .env file).
