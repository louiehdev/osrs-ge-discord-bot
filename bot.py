#bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from helpers import get_item_data, get_item_versions, parse_item_data, display_price_data_embed

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
  print(f'{bot.user} has connected successfully!')

@bot.command(name="price", help="Get important price information about an item from the OSRS Grand Exchange.")
async def price(ctx, *args):
  await ctx.send("Welcome to the OSRS Grand Exchange Price Checker!")
  
  def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
  
  try:
    item: str = " ".join(args)
    item_data: dict = get_item_data(item)
    item_versions = get_item_versions(item_data)
    price_data: dict
    if item_versions:
      await ctx.send(f"Multiple versions of {item} found. Please specify the version you want to check the price of: {item_versions}", ephemeral=True)
      msg = await bot.wait_for('message', check=check, timeout=30.0)
      item_version = msg.content
      price_data = parse_item_data(item_data, item_version)
    else:
      price_data = parse_item_data(item_data)
    await ctx.send(embed=display_price_data_embed(price_data))
  except Exception as e:
    await ctx.send(str(e))

bot.run(TOKEN)