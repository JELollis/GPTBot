# Replace with your API credentials
api_key = ""
bot_token = ""

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from openai import OpenAI

client = OpenAI(api_key=api_key)

# Set the OpenAI API key

# Initialize the Discord client with intents and commands extension
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
slash = SlashCommand(bot, sync_commands=True)  # This will create and sync commands on bot start-up

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    print("Message received:", message.content)  # Debug print statement

    if message.author == bot.user:
        return

    await bot.process_commands(message)  # Important for processing commands

@bot.command(name='answer')
async def regular_answer(ctx, *, question: str):
    # Use the API to answer the question
    response = client.completions.create(model="gpt-3.5-turbo",  # Choose an appropriate engine
    prompt=question,
    max_tokens=150)

    # Send the response back to the channel
    await ctx.send(response.choices[0].text)

@slash.slash(name="answer", description="Get an answer to a question")
async def slash_answer(ctx, question: str):
    # Use the API to answer the question
    response = client.completions.create(model="gpt-3.5-turbo",  # Choose an appropriate engine
    prompt=question,
    max_tokens=150)

    # Send the response back to the channel
    await ctx.send(response.choices[0].text)

# Run the bot with the new bot token
bot.run(bot_token)
