import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from Games.Wordle.wordle_game import WordleGame

# Load variables from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

prefix = '/'
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='amw', help='Start a letter guessing game.')
async def start_letter_guessing(ctx):
    # Send a message to choose difficulty level
    embed = discord.Embed(
        title='Choose Difficulty Level',
        description='React to this message to select the difficulty level:',
        color=0x3498db  # You can customize the color
    )

    embed.add_field(name=':smiley: Easy', value='Words up to 6 characters with hints and categories', inline=False)
    embed.add_field(name=':face_with_raised_eyebrow: Medium', value='Words up to 8 characters with hints and categories', inline=False)
    embed.add_field(name=':grimacing: Hard', value='Words up to 12 characters without hints and categories', inline=False)
    embed.add_field(name=':cat: Very Hard', value='Words of any length without hints and categories', inline=False)

    difficulty_message = await ctx.send(embed=embed)

    # Add reactions to the message
    reactions = ['😃', '🤨', '😬', '🐱']
    for reaction in reactions:
        await difficulty_message.add_reaction(reaction)

    # Wait for a reaction from the user
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions

    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=60, check=check)
    except asyncio.TimeoutError:
        return await ctx.send('Time is up. Please run the command again to start a new game.')

    # Map reactions to difficulty levels
    difficulty_mapping = {
        '😃': 'easy',
        '🤨': 'medium',
        '😬': 'hard',
        '🐱': 'veryhard'
    }

    difficulty = difficulty_mapping.get(str(reaction.emoji))
    if not difficulty:
        return await ctx.send('Invalid difficulty level. Please run the command again to start a new game.')

    # Start the Wordle game
    wordle_game = WordleGame(ctx, difficulty)
    await wordle_game.send_initial_message()
    await wordle_game.play_game()

bot.run(TOKEN)
