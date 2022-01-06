import discord
import word_lists.word_list_generator
import random
import renderer
import enchant
from datetime import datetime

client = discord.Client()
d = enchant.Dict("en_US")

date_format = "%d/%m/%y"
last_played_path = "last_played.txt"

def get_last_played():
    with open(last_played_path, 'r') as file:
        date_string = file.read()

    print("date string is is: {}".format(date_string))

    return datetime.strptime(date_string, date_format)

def set_last_played():
    today = datetime.today().strftime(date_format)
    print("today is: {}".format(today))

    with open(last_played_path, 'w') as file:
        file.write(today)

def generate_target_word(word_length):
    try:
        possible_words = word_lists.word_list_generator.get_list(int(word_length), 1000)
        return random.choice(possible_words)
    except IndexError as e:
        possible_words = word_lists.word_list_generator.get_list(word_length, e.args[0])
        if len(possible_words) > 0:
            return random.choice(possible_words)
        else:
            raise ValueError('Failed to get a word of that length')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!wordle'):
        args = message.content.split(' ')
        if len(args) != 2:
            await message.channel.send("**Usage: !wordle [length of word to guess]**")
        else:
            if args[1].isdigit(): 
                length = int(args[1])

                if length > 3 and length <= 10:
                    if get_last_played().date() != datetime.today().date():
                        await play_wordle(message, length)
                        set_last_played()
                    else:
                        await message.channel.send("**I hope you weren't trying to play Wordle more than once per day... ;)**")
                else:
                    await message.channel.send("**Word length should be between 3 and 10**")
            else:
                await message.channel.send("**Word length should be between 3 and 10**")
            
def validate_word(guess, word):
    result_string = ""
    for i in range(0, len(guess)):
        if guess[i] == word[i]:
            result_string += perfect_letter
        else:
            if guess[i] in word:
                result_string += correct_letter
            else:
                result_string += incorrect_letter

    return result_string

async def play_wordle(message, word_length):
    #This is ugly, don't @ me
    def check_for_guess(m):
        return m.content.startswith('!g') and m.channel == message.channel

    try:
        word = generate_target_word(word_length).upper()
        print("Your word is.... {}".format(word))
        guessed_letters = set()

        await message.channel.send("**Generated word, game starting - Use !g to guess, !giveup to quit**")

        guesses_remaining = word_length + 1

        while guesses_remaining > 0:  
            guess = ""
            in_dictionary = False

            while len(guess) != word_length or not in_dictionary:
                try:
                    msg = await client.wait_for('message', check=check_for_guess, timeout=300)
                    msg_args = msg.content.split(' ')

                    if msg_args[0] == '!giveup':
                        await message.channel.send("The word was...  {}".format(word))
                        return

                    if msg_args[0] == '!g':
                        if len(msg_args) == 2:
                            guess = msg_args[1]
                            
                            if len(guess) != word_length:
                                await message.channel.send("*Invalid length guess*")
                            else:
                                in_dictionary = d.check(guess)
                                guess = guess.upper()

                                if not in_dictionary:
                                    await message.channel.send("*Word not in the dictionary*")
                        else:
                            await message.channel.send("*You need to guess a word*")
                except:
                    await message.channel.send("No guesses, stopping game...  :(")
                    return

            guesses_remaining -= 1

            for l in guess:
                guessed_letters.add(l)

            if guess != word:
                renderer.generate_guess_image(guess, word)
                renderer.generate_letters_image(guessed_letters, word)
                await message.channel.send("**{} guesses remaining**".format(guesses_remaining), file=discord.File('guess_result.png'))
                await message.channel.send(file=discord.File('letters_used.png'))
            else:
                renderer.generate_guess_image(guess, word)
                await message.channel.send("**You guessed correctly!**".format(guesses_remaining), file=discord.File('guess_result.png'))
                return

        await message.channel.send("**You're out of guesses, game over! The word was...  {}**".format(word))

    except ValueError as e:
        await message.channel.send('*{}*'.format(e.args[0]))
        return

client.run('[TOKEN]')
