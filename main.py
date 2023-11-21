TOKEN = 'MTE3NjU3NDk0Njc5Mzc2Njk4Mw.GIOFwC.kocaYQSsk_2kze0B1hT231o18iVAp1KMXaQ0kw'

import discord
from discord.ext import commands
import random
import asyncio

# TOKEN = 'YOUR_TOKEN'
prefix = '/'  # Set a prefix for the command (e.g., '/')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='game', help='Start a letter guessing game.')
async def start_letter_guessing(ctx):
    # Choose a random word and category for the game
    word_to_guess, category = get_random_word()
    word_to_guess = word_to_guess.lower()  # Convert word to lowercase
    category = category.lower()  # Convert category to lowercase

    word_len = len(word_to_guess)

    # Set the maximum number of attempts
    max_attempts = word_len * 2

    # Initialize the guessed word with '-'
    guessed_word = ['-']

    # Fill the remaining characters with '-'
    for _ in range(word_len - 1):
        guessed_word.append('-' if word_to_guess[_].isalpha() else word_to_guess[_])

    # Choose one hint character randomly from unfilled characters
    hint_character_index = random.choice([i for i, char in enumerate(guessed_word) if char == '-'])
    guessed_word[hint_character_index] = ':cat:'

    # Display the initial message and guessed word in an embed with the hint
    embed = discord.Embed(title='ยินดีต้อนรับเข้าสู่ OMOWO Game', color=0x00ff00)
    embed.add_field(name='Category', value=category, inline=False)
    embed.add_field(name='Word to Guess', value=' '.join(guessed_word), inline=False)
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
                guessed_word[hint_character_index] = ':cat:'
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
            embed.add_field(name='Category', value=category, inline=False)
            embed.add_field(name='Word to Guess', value=' '.join(guessed_word), inline=False)
            embed.add_field(name='Results', value=f'Correct Attempts: {correct_attempts}\nIncorrect Attempts: {incorrect_attempts}', inline=False)
            embed.set_footer(text=f'{word_len * 2 - attempt - 1} attempts remaining')
            await message.edit(embed=embed)

            # Check if the word has been completely guessed
            if '-' not in guessed_word:
                await ctx.send(f':cat: เก่งมากๆเลยยยย!ว้าวๆๆๆ :cat: คุณ!! ได้ทายคำว่า: {word_to_guess} from the category: {category}')
                break

        else:
            # Send a specific message when attempts reach 0
            await ctx.send(f'Oh ohh! You losttttt loser loser loser ... I\'m just kidding :) the word is: {word_to_guess} from the category: {category}')

    except asyncio.TimeoutError:
        await ctx.send(f'ว้าาา หมดเวลาสนุกแล้วสิ ไปเรียนภาษาอังกฤษแล้วค่อยมาเล่นใหม่นะ55555 คำที่ถูกคือ : {word_to_guess} from the category: {category}')

# Add more helper functions as needed
def get_random_word():
    # Replace this with a function that retrieves a random word and category
    # You can use external APIs or a predefined list of words with categories
    word_list = [
        ('apple', 'Fruit'), ('banana', 'Fruit'), ('orange', 'Fruit'), ('grape', 'Fruit'), ('kiwi', 'Fruit'),
        ('mango', 'Fruit'), ('lemon', 'Fruit'), ('peach', 'Fruit'), ('cherry', 'Fruit'), ('pineapple', 'Fruit'),
        ('watermelon', 'Fruit'), ('strawberry', 'Fruit'), ('blueberry', 'Fruit'), ('raspberry', 'Fruit'), ('blackberry', 'Fruit'),
        ('avocado', 'Vegetable'), ('cucumber', 'Vegetable'), ('tomato', 'Vegetable'), ('broccoli', 'Vegetable'), ('spinach', 'Vegetable'),
        ('carrot', 'Vegetable'), ('potato', 'Vegetable'), ('onion', 'Vegetable'), ('garlic', 'Vegetable'), ('mushroom', 'Vegetable'),
        ('eggplant', 'Vegetable'), ('bellpepper', 'Vegetable'), ('lettuce', 'Vegetable'), ('cauliflower', 'Vegetable'), ('zucchini', 'Vegetable'),
        ('pumpkin', 'Vegetable'), ('asparagus', 'Vegetable'), ('radish', 'Vegetable'), ('celery', 'Vegetable'), ('beet', 'Vegetable'),
        ('cucumber', 'Vegetable'), ('egg', 'Other'), ('bacon', 'Other'), ('sausage', 'Other'), ('cheese', 'Other'),
        ('bread', 'Other'), ('pasta', 'Other'), ('rice', 'Other'), ('chicken', 'Protein'), ('fish', 'Protein'),
        ('beef', 'Protein'), ('shrimp', 'Protein'), ('pizza', 'Dish'), ('sandwich', 'Dish'), ('salad', 'Dish'),
        ('lion', 'Animal'), ('elephant', 'Animal'), ('giraffe', 'Animal'), ('tiger', 'Animal'), ('zebra', 'Animal'),
        ('monkey', 'Animal'), ('kangaroo', 'Animal'), ('panda', 'Animal'), ('koala', 'Animal'), ('penguin', 'Animal'),
        ('parrot', 'Animal'), ('dolphin', 'Animal'), ('crocodile', 'Animal'), ('camel', 'Animal'), ('kangaroo', 'Animal'),
        ('australia', 'Country'), ('canada', 'Country'), ('india', 'Country'), ('brazil', 'Country'), ('japan', 'Country'),
        ('france', 'Country'), ('germany', 'Country'), ('italy', 'Country'), ('russia', 'Country'), ('spain', 'Country'),
        ('pizza', 'Food'), ('sushi', 'Food'), ('burger', 'Food'), ('pasta', 'Food'), ('icecream', 'Food'),
        ('cake', 'Food'), ('coffee', 'Food'), ('tea', 'Food'), ('chocolate', 'Food'), ('sandwich', 'Food'),
        ('computer', 'Thing'), ('phone', 'Thing'), ('book', 'Thing'), ('car', 'Thing'), ('camera', 'Thing'),
        ('guitar', 'Thing'), ('watch', 'Thing'), ('glasses', 'Thing'), ('shoes', 'Thing'), ('hat', 'Thing')
    ]

    return random.choice(word_list)

bot.run(TOKEN)