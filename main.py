import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

my_secret = os.environ['TOKEN']
sad_words = ["sad","depressed","kill","suicide","angry","mad","unhappy","miserable","depressing"]

starter_encouragments =[
  "cheer up mate",
  "Hang in there buddy",
  "fuck the world bruv"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quotes():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " ~" + json_data[0]['a']
    return(quote)

def update_encouragments(encouraging_message):
  if "encouragments" in db.keys():
    encouragments = db["encouragments"]
    encouragments.append(encouraging_message)
    db["encouragments"] = encouragments
  else:
    db["encouragments"] = [encouraging_message]

def delete_encouragment(index):
  encouragments = db["encouragments"]
  if len(encouragments) > index:
    del encouragments[index]
    db["encouragments"] = encouragments


@client.event
async def on_ready():
    print('We have logged in as {0,user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$hello'):
        await message.channel.send('Hello !')

    if msg.startswith('$inspire'):
        quote = get_quotes()
        await message.channel.send(quote)

    if db["responding"]:
      options = starter_encouragments
      if "encouragements" in db.keys():
        options = options + db["encouragements"]

    #  if "encouragments" in db.keys():
    #    options = options.extend(db["encouragements"])
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragments(encouraging_message)
      await message.channel.send("new enouraging message added")

    if msg.startswith("$del"):
      encouragments = []
      if "encouragments" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragment(index)
        encouragments = db["encouragments"]
      await message.channel.send(encouragments)

    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$responding"):
      value = msg.split("$responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")

keep_alive()
client.run(my_secret)
