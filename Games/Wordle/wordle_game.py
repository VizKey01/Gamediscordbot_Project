import discord
from discord.ext import commands
import random
import asyncio
from .word_list import get_random_word

class WordleGame:
    def __init__(self, ctx, difficulty):
        self.ctx = ctx
        self.difficulty = difficulty
        self.word_to_guess, self.category = get_random_word(difficulty)
        self.word_to_guess = self.word_to_guess.lower()
        self.category = self.category.lower()
        self.word_len = len(self.word_to_guess)
        self.max_attempts = self.word_len + 6
        self.guessed_word = [':cat:']
        for _ in range(self.word_len - 1):
            self.guessed_word.append(':cat:' if self.word_to_guess[_].isalpha() else self.word_to_guess[_])

        self.timeout_seconds = 90
        self.incorrect_attempts = 0
        self.correct_attempts = 0

    # hint setting
    async def send_initial_message(self):

        # check to not add hint word
        if self.difficulty == 'easy' or self.difficulty == 'medium':
            hint_character_index = random.choice([i for i, char in enumerate(self.guessed_word) if char == ':cat:'])
            self.guessed_word[hint_character_index] = self.word_to_guess[hint_character_index]

        embed = discord.Embed(title='ยินดีต้อนรับเข้าสู่ OMOWO Game', color=0x00ff00)
        if self.difficulty != 'veryhard':
            embed.add_field(name='Category', value=self.category, inline=False)

        embed.add_field(name='Word to Guess', value=' '.join(self.guessed_word), inline=False)
        if self.difficulty != 'hard' and self.difficulty != 'veryhard':
            embed.add_field(name='Results', value=f'Game started! Here\'s a hint: {self.guessed_word[hint_character_index]}', inline=False)

        embed.set_footer(text=f'{self.word_len + 6} attempts remaining')
        self.message = await self.ctx.send(embed=embed)

    async def play_game(self):
        try:
            for attempt in range(self.max_attempts):
                def check(msg):
                    return msg.channel == self.ctx.channel and msg.author == self.ctx.author and msg.content.isalpha() and len(msg.content) == 1

                guess_msg = await self.ctx.bot.wait_for('message', check=check, timeout=self.timeout_seconds)

                guessed_letter = guess_msg.content.lower()

                if not guessed_letter.isalpha():
                    self.guessed_word[0] = ':cat:'
                else:
                    correct_guesses = [i for i, char in enumerate(self.word_to_guess) if char == guessed_letter]
                    if not correct_guesses:
                        self.incorrect_attempts += 1
                    else:
                        self.correct_attempts += 1

                    for index in correct_guesses:
                        self.guessed_word[index] = guessed_letter

                embed = discord.Embed(title='ยินดีต้อนรับเข้าสู่ OMOWO Game', color=0x00ff00)
                if self.difficulty != 'veryhard':
                    embed.add_field(name='Category', value=self.category, inline=False)
                embed.add_field(name='Word to Guess', value=' '.join(self.guessed_word), inline=False)
                embed.add_field(name='Results', value=f'Correct Attempts: {self.correct_attempts}\nIncorrect Attempts: {self.incorrect_attempts}', inline=False)
                embed.set_footer(text=f'{self.word_len + 6 - attempt - 1} attempts remaining')
                await self.message.edit(embed=embed)

                if ':cat:' not in self.guessed_word:
                    await self.ctx.send(f'เก่งมากเลยยยย! ว้าวๆๆๆ คุณ!! ได้ทายคำว่า: {self.word_to_guess}')
                    break

            else:
                await self.ctx.send(f'Oh ohh! You losttttt loser loser loser ... I\'m just kidding :) the word is: {self.word_to_guess} ')

        except asyncio.TimeoutError:
            await self.ctx.send(f'ว้าาา หมดเวลาสนุกแล้วสิ ไปเรียนภาษาอังกฤษแล้วค่อยมาเล่นใหม่นะ55555 คำที่ถูกคือ: {self.word_to_guess}')
