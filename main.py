import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "kms", "kys", "depression", "despair", "lonely"]

starter_encouragements = ["cheer up!", "Hang in there!", "You are a great person/bot!", "ily!", "<3", ":)", "I'll always be there :)"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote=json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
  else:
    db["encouragements"]=[encouraging_message]

def del_encour(index):
  encour = db["encouragements"]
  if len(encour) > index:
    del encour[index]
    db["encouragements"] = encour

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith("$responding"):
      value = msg.split("$responding ", 1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      if value.lower() == "false":
        db["responding"] = False
        await message.channel.send("Responding is off.")
  
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if message.content.startswith('$hello'):
      await message.channel.send('Hello!')

    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ", 1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del", 1)[1])
        del_encour(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    
    if message.content.startswith('$help'):
      await message.channel.send("Here's what I can do for you:\nType \"$hello\" if you want to say hi to me!\nType \"$inspire\" if you would like an inspirational quote!\nI will automatically send an inspiring text if I detect a sad message.\nYou can add to the list of inspiring messages by typing \"$new\" followed by the inspiring message.\nYou can also delete an inspiring message by typing \"$del\" followed by the number of your message.\nTo find out the number type \"$list\" and start counting from 0 at the first elements.\nIf I am interefering with your messages then type \"$responding\" followed by true/false to make me start/stop talking.\nAlso beep boop... I'm Udayan... beep boop")
my_secret = os.environ['TOKEN']
keep_alive()
client.run(os.getenv('TOKEN'))
