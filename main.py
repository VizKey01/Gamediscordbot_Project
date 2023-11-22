import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio

# Load variables from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

prefix = '/'
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='game', help='Start a letter guessing game.')
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

    # Choose a random word and category for the game based on difficulty
    word_to_guess, category = get_random_word(difficulty)
    word_to_guess = word_to_guess.lower()  # Convert word to lowercase
    category = category.lower()  # Convert category to lowercase

    word_len = len(word_to_guess)

    # Set the maximum number of attempts
    max_attempts = word_len * 2

    # Initialize the guessed word with ':cat:'
    guessed_word = [':cat:']

    # Fill the remaining characters with ':cat:'
    for _ in range(word_len - 1):
        guessed_word.append(':cat:' if word_to_guess[_].isalpha() else word_to_guess[_])

    # Choose one hint character randomly from unfilled characters
    if difficulty == 'easy' or difficulty == 'medium':
        hint_character_index = random.choice([i for i, char in enumerate(guessed_word) if char == ':cat:'])
        guessed_word[hint_character_index] = word_to_guess[hint_character_index]

    # Display the initial message and guessed word in an embed with the hint
    embed = discord.Embed(title='ยินดีต้อนรับเข้าสู่ OMOWO Game', color=0x00ff00)
    if difficulty != 'veryhard':
        embed.add_field(name='Category', value=category, inline=False)
    embed.add_field(name='Word to Guess', value=' '.join(guessed_word), inline=False)
    if difficulty != 'hard' and difficulty != 'veryhard':
        embed.add_field(name='Results', value=f'Game started! Here\'s a hint: {guessed_word[hint_character_index]}', inline=False)
    embed.set_footer(text=f'{word_len * 2} attempts remaining')
    message = await ctx.send(embed=embed)

    # Set a timeout for 1.5 minutes
    timeout_seconds = 90
    incorrect_attempts = 0
    correct_attempts = 0

    try:
        for attempt in range(max_attempts):
            # Wait for a message from the same channel and author
            def check(msg):
                return msg.channel == ctx.channel and msg.author == ctx.author and msg.content.isalpha() and len(msg.content) == 1

            guess_msg = await bot.wait_for('message', check=check, timeout=timeout_seconds)

            # Get the guessed letter
            guessed_letter = guess_msg.content.lower()

            # Check if the guessed letter is correct
            if not guessed_letter.isalpha():
                guessed_word[0] = ':cat:'
            else:
                correct_guesses = [i for i, char in enumerate(word_to_guess) if char == guessed_letter]
                if not correct_guesses:
                    incorrect_attempts += 1
                else:
                    correct_attempts += 1

                for index in correct_guesses:
                    guessed_word[index] = guessed_letter

            # Update the guessed word and display results in an embed
            embed = discord.Embed(title='ยินดีต้อนรับเข้าสู่ OMOWO Game', color=0x00ff00)
            if difficulty != 'veryhard':
                embed.add_field(name='Category', value=category, inline=False)
            embed.add_field(name='Word to Guess', value=' '.join(guessed_word), inline=False)
            embed.add_field(name='Results', value=f'Correct Attempts: {correct_attempts}\nIncorrect Attempts: {incorrect_attempts}', inline=False)
            embed.set_footer(text=f'{word_len * 2 - attempt - 1} attempts remaining')
            await message.edit(embed=embed)

            # Check if the word has been completely guessed
            if ':cat:' not in guessed_word:
                await ctx.send(f'เก่งมากเลยยยย! ว้าวๆๆๆ คุณ!! ได้ทายคำว่า: {word_to_guess}')
                break

        else:
            # Send a specific message when attempts reach 0
            await ctx.send(f'Oh ohh! You losttttt loser loser loser ... I\'m just kidding :) the word is: {word_to_guess} ')

    except asyncio.TimeoutError:
        await ctx.send(f'ว้าาา หมดเวลาสนุกแล้วสิ ไปเรียนภาษาอังกฤษแล้วค่อยมาเล่นใหม่นะ55555 คำที่ถูกคือ: {word_to_guess}')

def get_random_word(difficulty='medium'):
    # Replace this with a function that retrieves a random word and category based on difficulty
    # You can use external APIs or a predefined list of words with categories
    word_list = [
    ('spain', 'Country'), ('australia', 'Country'), ('thailand', 'Country'), ('canada', 'Country'), ('brazil', 'Country'),
    ('nigeria', 'Country'), ('italy', 'Country'), ('russia', 'Country'), ('japan', 'Country'), ('india', 'Country'),
    ('hamburger', 'Food'), ('pasta', 'Food'), ('sushi', 'Food'), ('taco', 'Food'), ('icecream', 'Food'),
    ('laptop', 'Technology'), ('camera', 'Technology'), ('robot', 'Technology'), ('drone', 'Technology'), ('satellite', 'Technology'),
    ('guitar', 'Thing'), ('bookshelf', 'Thing'), ('lampshade', 'Thing'), ('telescope', 'Thing'), ('shoes', 'Thing'),
    ('programming', 'Field of Study'), ('chemistry', 'Field of Study'), ('history', 'Field of Study'), ('psychology', 'Field of Study'), ('mathematics', 'Field of Study'),
    ('nintendo', 'Game'), ('minecraft', 'Game'), ('fortnite', 'Game'), ('overwatch', 'Game'), ('pokemon', 'Game'),
    ('carrot', 'Vegetable'), ('cucumber', 'Vegetable'), ('tomato', 'Vegetable'), ('broccoli', 'Vegetable'), ('spinach', 'Vegetable'),
    ('pomegranate', 'Fruit'), ('watermelon', 'Fruit'), ('strawberry', 'Fruit'), ('blueberry', 'Fruit'), ('pineapple', 'Fruit'),
    ('parrot', 'Animal'), ('elephant', 'Animal'), ('giraffe', 'Animal'), ('kangaroo', 'Animal'), ('penguin', 'Animal'),
    ('museum', 'Place'), ('library', 'Place'), ('park', 'Place'), ('beach', 'Place'), ('castle', 'Place'),
    ('computer', 'Thing'), ('glasses', 'Thing'), ('backpack', 'Thing'), ('umbrella', 'Thing'), ('bracelet', 'Thing'),
    ('blockchain', 'Technology'), ('artificialintelligence', 'Technology'), ('augmentedreality', 'Technology'), ('biotechnology', 'Technology'), ('nanotechnology', 'Technology'),
    ('football', 'Sport'), ('basketball', 'Sport'), ('tennis', 'Sport'), ('golf', 'Sport'), ('cycling', 'Sport'),
    ('lobster', 'Food'), ('steak', 'Food'), ('pizza', 'Food'), ('sushi', 'Food'), ('chocolate', 'Food'),
    ('australia', 'Country'), ('thailand', 'Country'), ('canada', 'Country'), ('brazil', 'Country'), ('nigeria', 'Country'),
    ('pyramid', 'Place'), ('eiffeltower', 'Place'), ('colosseum', 'Place'), ('machupicchu', 'Place'), ('greatwall', 'Place'),
    ('astronaut', 'Occupation'), ('doctor', 'Occupation'), ('chef', 'Occupation'), ('engineer', 'Occupation'), ('artist', 'Occupation'),
    ('penguin', 'Animal'), ('koala', 'Animal'), ('zebra', 'Animal'), ('panda', 'Animal'), ('dolphin', 'Animal')
]

    if difficulty == 'easy':
        # Filter words based on difficulty level
        word_list = [(word, category) for word, category in word_list if len(word) <= 6]
    elif difficulty == 'medium':
        word_list = [(word, category) for word, category in word_list if 6 < len(word) <= 8]
    elif difficulty == 'hard':
        word_list = [(word, category) for word, category in word_list if 8 < len(word) <= 12]
    elif difficulty == 'veryhard':
        word_list = [(word, category) for word, category in word_list if len(word) > 12]

    if not word_list:
        raise ValueError(f'No words available for the selected difficulty level: {difficulty}')

    return random.choice(word_list)

bot.run(TOKEN)
