#!/usr/bin/env python

import discord
import os
from dotenv import load_dotenv
from llm_wrapper import LLMWrapper

load_dotenv(override=True)

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
client = discord.Client(intents=intents)

MESSAGES = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

async def ask_guppi(message):
  llm = LLMWrapper('openai', 'gpt-3.5-turbo')
  # llm = LLMWrapper('ollama', 'dolphin2.2-mistral')

  MESSAGES.append({'role': 'user', 'content': message})

  reply = ''

  for response in llm.send_message(MESSAGES):
    if response['role'] == 'assistant' and response['content'] != None:
      reply += response['content']

    if response['done']:
      MESSAGES.append({'role': 'assistant', 'content': reply})
      break
  return reply

@client.event
async def on_ready():
  print(f'Logged on as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
     return

  async with message.channel.typing():
    try:
      reply = await ask_guppi(message.content)
      if reply:
        await message.channel.send(reply)
    except Exception as e:
      await message.channel.send(e)

client.run(TOKEN)
