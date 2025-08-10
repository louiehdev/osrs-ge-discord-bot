import requests
import re
import discord
from constants import BASE_URL, GE_URL, QUERY_PARAMS, PARSE_PARAMS, HEADERS, DATA_PARAMS

def get_page_id(item):
  query_params = QUERY_PARAMS.copy()
  query_params["srsearch"] = item
  response = requests.get(BASE_URL, params=query_params, headers=HEADERS)
  if response is None or response.status_code != 200:
    raise Exception("Error: Could not retrieve item data. Please check the item name or ID and try again.")
  data = response.json()
  if data["query"]["search"][0]["title"].lower() != item.lower() and item.lower() not in data["query"]["search"][0]["title"].lower():
    options = "".join([f"{data['query']['search'][i]['title']}, " for i in range(len(data["query"]["search"]))])
    raise Exception(f"Error: Did you mean to search for: {options}?")
  return data["query"]["search"][0]["pageid"]

def get_item_data(item):
  page_id = get_page_id(item)
  parse_params = PARSE_PARAMS.copy()
  parse_params["pageid"] = page_id
  response = requests.get(BASE_URL, params=parse_params, headers=HEADERS)
  if response is None or response.status_code != 200:
    raise Exception("Error: Could not retrieve item data. Please check the item name or ID and try again.")
  data = response.json()
  infobox_search = re.search(r'\{\{Infobox Item(.*?)\n\}\}', data["parse"]["wikitext"]["*"], re.DOTALL)
  if infobox_search:
    data_search = re.findall(r'\|(\w+)\s*=\s*(.*?)\n', infobox_search.group())
    data_dict = dict(data_search)
    return data_dict

def get_item_price_data(item_data: dict):
  response = requests.get(f'{GE_URL}{item_data["id"]}', headers=HEADERS)

  if response is None or response.status_code != 200:
    raise Exception("Error: Could not retrieve item price. Please check the item name or ID and try again.")
  
  price_data = response.json()['item']
  if not isinstance(price_data["current"], dict):
    price_data["current"] = {"price": str(price_data["current"])}
  
  return price_data

def get_item_versions(item_data: dict):
  if "id" not in item_data:
    versions = ""
    item_version_count = len(re.findall(r'version', str(item_data)))
    if item_version_count > 0:
      versions = "".join([f"{i}. {item_data[f'name{i}']}, " for i in range(1, item_version_count + 1)])
    return versions

def parse_item_data(item_data: dict, item_version=None):
  full_data = item_data.copy()
  if item_version:
    item_version = str(item_version)

    id_key = f"id{item_version}"
    examine_key = f"examine{item_version}"
    value_key = f"value{item_version}" if f"value{item_version}" in full_data else "value"

    full_data["id"] = full_data.get(id_key)
    full_data["examine"] = full_data.get(examine_key)
    full_data["value"] = full_data.get(value_key)

  price_data = get_item_price_data(full_data)
  full_data.update(price_data)
  parsed_data = {key: value for key, value in full_data.items() if key in DATA_PARAMS}
  parsed_data["price"] = full_data["current"]["price"]
  parsed_data["highalch"] = round(float(full_data["value"]) * 0.6)
  parsed_data["lowalch"] = round(float(full_data["value"]) * 0.4)
  nature_rune_response = requests.get(f'{GE_URL}561', headers=HEADERS)
  if nature_rune_response:
    parsed_data["naturerune"] = int(nature_rune_response.json()["item"]["current"]["price"])
  print("[DEBUG] Parsed data:", parsed_data)
  return parsed_data

def price_to_int(price):
  price_string = str(price)
  match price_string[-1]:
    case "k":
      return round(float(price_string[:-1]) * 1000)
    case "m":
      return round(float(price_string[:-1]) * 1000000)
    case "b":
      return round(float(price_string[:-1]) * 1000000000)
    case _:
      price_string = price_string.replace(",", "")
      return int(price_string)

def display_price_data(item_data: dict):
  name = (f"Item Name: {item_data['name']}")
  desc = (f"Description: {item_data['examine']}")
  id = (f"Item ID: {item_data['id']}")
  price = (f"Current Price: {item_data['price']} GP")
  highalch = (f"High Alch Value: {item_data['highalch']} GP")
  highalch_profit = (f"High Alch Profit: {int(item_data['highalch']) - price_to_int(item_data['price']) - item_data['naturerune']} GP")
  return '\n'.join([name, desc, id, price, highalch, highalch_profit])

def display_price_data_embed(item_data: dict):
  osrs_gold = discord.Color.from_rgb(255, 204, 51)

  embed = discord.Embed(title=item_data["name"], description=item_data["examine"], color=osrs_gold)

  embed.set_image(url=f"https://services.runescape.com/m=itemdb_oldschool/obj_sprite.gif?id={item_data['id']}")

  embed.add_field(name="💰 Current Price", value=f"{item_data['price']} GP", inline=True)
  embed.add_field(name="🔮 High Alch", value=f"{item_data['highalch']} GP", inline=True)
  embed.add_field(name="🔮 Low Alch", value=f"{item_data['lowalch']} GP", inline=True)
  embed.add_field(name="🌿 Nature Rune Price", value=f"{item_data['naturerune']} GP", inline=True)
  embed.add_field(name="📈 High Alch Profit", value=f"{int(item_data['highalch']) - price_to_int(item_data['price']) - item_data['naturerune']} GP", inline=True)
  embed.add_field(name="🆔 Item ID", value=str(item_data['id']), inline=True)

  embed.set_footer(text="OSRS Grand Exchange - Data from the Official API & Wiki")

  return embed