# botv2.py

# python packages
import random
import os
import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import asyncio
import requests
import ast
import logging
from googleapiclient.discovery import build

# Local Packages
from mypackages import greetings, quiz, quotes, textfaces, profanities

triviaQuizQ = quiz.trivia_quiz_set
triviaQuizA = quiz.trivia_answers
managementQuizQ = quiz.management_quiz_set
managementQuizA = quiz.management_answers

logging.basicConfig(format='%(asctime)s : %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

vname = "mangoBot (17/9/2020)"
discordToken = os.environ['token']
clashToken = os.environ['clashToken']
youtubeToken = os.environ['youtubeToken']

# ==================================================================================================================== #

# Description for commands only usable by me
me = "Only usable by mangoomeh"

# Command prefix
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove default help command in order to customise it
bot.remove_command('help')

# Function that checks if the message is sent by me
def owner(m):
    return m.author.id == 311159834823360512


# Function that checks if the message is sent by any of the developers
def dev(m):
    a = 334645578111647746
    b = 311159834823360512
    c = 372024452042457108
    return m.author.id == a or m.author.id == b or m.author.id == c


# Bot event that shows that the bot has connected
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# Bot event that processes messages sent in the channel
@bot.event
async def on_message(message):
    # This stops the code if the message is sent by the bot itself
    if message.author == bot.user:
        return

    # This block of code processes message content
    mm = message.content
    mm_words = mm.lower().split()

    for i in profanities.profanities:
        if i in mm_words:
            logging.info(str(mm))
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please mind your language :)", delete_after=3)
            return

    # This block of code checks for relevant keywords and sends emote.png to the channel
    if mm == "HAHA":
        await message.channel.send(file=discord.File('images/haha.png'), delete_after=3)
        return
    elif mm.lower() == "sad":
        await message.channel.send(file=discord.File('images/sad.png'), delete_after=3)
        return
    elif mm.lower() == "pig":
        await message.channel.send(file=discord.File('images/pig.png'), delete_after=3)
        return
    elif mm == "HUH":
        await message.channel.send(file=discord.File('images/wth.png'), delete_after=3)
        return
    elif mm.lower() == "hear ye":
        await message.channel.send(file=discord.File('images/hearye.png'), delete_after=3)
        return
    elif mm.lower() == "omg":
        await message.channel.send(file=discord.File('images/omg.png'), delete_after=3)
        return
    elif mm.lower() == "sleep":
        await message.channel.send(file=discord.File('images/sleep.png'), delete_after=3)
        return
    elif mm.lower() == "phew":
        await message.channel.send(file=discord.File('images/phew.png'), delete_after=3)
        return
    else:
        await bot.process_commands(message)


# This block of code is to test functions (pass is used when nothing is to be tested)
@bot.command(name='test', description=me)
@commands.check(owner)
async def test(ctx):
    pass


# This is the command that shows all commands only usable by me (only usable by me)
@bot.command(name="z", description=me)
@commands.check(owner)
async def z(ctx):
    await ctx.message.delete()
    helptext = "```"
    helptext += "{0:8} | {1}\n".format("Commands", "Function")
    for command in bot.commands:
        x = str(command.description) == me
        if x:
            helptext += "!{0:7} | {1}\n".format(str(command), str(command.description))
    helptext += "```"
    await ctx.send(helptext, delete_after=3)


# This is the command to list all users in the channel (only usable by me)
@bot.command(name='zuser', description=me)
@commands.check(owner)
async def getuser(ctx):
    await ctx.message.delete()
    x = ctx.channel.members
    botmsg = "Members in the Channel:\n"
    for i in x:
        a = i.name
        b = i.id
        c = f"{a}: {b}\n"
        botmsg += c
    await ctx.send(botmsg, delete_after=15)


# This is the command to clear mangoBot messages (only usable by me)
@bot.command(name='zclear', description=me)
@commands.check(owner)
async def mangoclear(ctx, a: int):
    await ctx.message.delete()
    messages = ctx.channel.history().filter(lambda m: m.author == bot.user)
    limit = a
    deleted = 0
    async for x in messages:
        if deleted >= limit:
            await ctx.send(f"{deleted} message(s) deleted.")
            break
        await x.delete()
        deleted += 1


# This is the message clearing command available to developers only
@bot.command(name='zc', description="developers only")
@commands.check(dev)
async def overclear(ctx):
    def check(m):
        return m.author == ctx.author

    await ctx.message.delete()

    # Ask for whose messages to delete
    members = ctx.channel.members
    botmsg = "Whose messages are we deleting?\n\n"
    for i in range(len(members)):
        line = f"({i + 1}) {members[i].name}: {members[i].id}\n"
        botmsg += line
    botmsg = await ctx.send(botmsg)
    msg = await bot.wait_for('message', check=check)
    await botmsg.delete()
    await msg.delete()

    # Ask for number of messages to delete
    index = int(msg.content) - 1
    messages = ctx.channel.history().filter(lambda m: m.author.id == members[index].id)
    botmsg = await ctx.send('How many messages?')
    msg = await bot.wait_for('message', check=check)
    limit = int(msg.content)
    await botmsg.delete()
    await msg.delete()

    # Commence delete
    deleted = 0
    async for x in messages:
        if deleted >= limit:
            await ctx.send(f"{deleted} message(s) deleted.", delete_after=3)
            break
        await x.delete()
        deleted += 1


@bot.command(name="help", description="Shows this message")
async def h(ctx):
    await ctx.message.delete()
    helptext = "```"
    helptext += "{0:8} | {1}\n".format("Commands", "Function")
    for command in bot.commands:
        x = str(command.description) == me
        if not x:
            helptext += "!{0:7} | {1}\n".format(str(command), str(command.description))
    helptext += "```"
    await ctx.send(helptext, delete_after=60)


@bot.command(name='ver', description='Shows current version')
async def version(ctx):
    await ctx.message.delete()
    await ctx.send("Current Build: " + vname, delete_after=5)


@bot.command(name='time', description='Date/Time')
async def time(ctx):
    await ctx.message.delete()
    now = datetime.now(timezone('Asia/Singapore'))
    response = now.strftime("%H:%M\n%d %B %Y")
    await ctx.send(ctx.author.mention + "\n" + response, delete_after=10)


@bot.command(name='m', description='Math Quiz')
async def math(ctx):
    await ctx.message.delete()
    await ctx.send("While in a question, type 'exit' to stop the quiz.", delete_after=5)

    def check(m):
        return m.author == ctx.message.author

    while True:
        a = random.randint(1, 99)
        b = random.randint(50, 99)
        c = random.randint(1, 5)
        d = random.randint(1, 5)
        question = f"{a} x ({c}+{d}) + {b} = ?"
        answer = str(a * (c + d) + b)
        botmsg1 = await ctx.send(question)

        try:
            msg = await bot.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            botmsg2 = await ctx.send(f'Time is up. Answer: {answer}')
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
        else:
            if msg.content.lower() == 'exit':
                await msg.delete()
                await botmsg1.delete()
                return
            elif msg.content == answer:
                botmsg2 = await ctx.send("That's right!")
                await asyncio.sleep(3)
                await botmsg1.delete()
                await botmsg2.delete()
                await msg.delete()
            else:
                botmsg2 = await ctx.send(f"The correct answer is: {answer}")
                await asyncio.sleep(5)
                await botmsg1.delete()
                await botmsg2.delete()
                await msg.delete()


@bot.command(name='u', description='Youtube')
async def youtube(ctx):
    await ctx.message.delete()
    max_results = 6

    def check(m):
        return m.author == ctx.author

    botmsg = await ctx.send("Your search?")
    try:
        msg = await bot.wait_for('message', check=check, timeout=30)
        await botmsg.delete()
        await msg.delete()
    except asyncio.TimeoutError:
        botmsg2 = (await ctx.send("Timeout. Try again at !u."))
        await asyncio.sleep(5)
        await botmsg.delete()
        await botmsg2.delete()
        return

    query = msg.content
    key = youtubeToken
    service = build('youtube', 'v3', developerKey=key)
    req = service.search().list(
            part='snippet',
            q=query,
            maxResults=6,
            type='video'
        )
    res = req.execute()
    res_formatted = []
    for i in res['items']:
        res_formatted.append([i['snippet']['title'], 'https://youtube.com/watch?v='+ i['id']['videoId']])

    print(res_formatted)
    botmsg = ""
    for i in range(len(res_formatted)):
        botmsg += "{}. {}\n".format(i+1, res_formatted[i][0])

    botmsg1 = await ctx.send(botmsg)
    try:
        msg = await bot.wait_for('message', check=check, timeout=30)
        await botmsg1.delete()
        await msg.delete()
        index = int(msg.content)

    except asyncio.TimeoutError:
        await botmsg1.delete()
        await ctx.send('Timeout.', delete_after=5)
        return
    except ValueError:
        await ctx.send('Invalid selection.', delete_after=5)
        await asyncio.sleep(5)
        await botmsg1.delete()
    else:
        await ctx.send(res_formatted[index - 1][1])

@bot.command(name='c', description='Delete message')
async def clear(ctx, *args):
    await ctx.message.delete()

    def check(m):
        return m.author == ctx.author

    messages = ctx.channel.history().filter(lambda m: check(m))
    deleted = 0

    # Case 1: !c used without additional arguments
    if len(args) == 0:
        limit = 1
        async for x in messages:
            if deleted >= limit:
                await ctx.send(f"{deleted} message(s) deleted.", delete_after=3)
                break
            await x.delete()
            deleted += 1
        return

    # Case 2: !c used with arguments
    else:
        # Check if argument is an integer
        try:
            limit = int(args[0])
        # Give warning message if argument is not an integer and stop deleting
        except ValueError:
            await ctx.send("Invalid. Careful, !c is a delete command.", delete_after=5)
            return

        # Give warning if user tries to delete more than 10 messages
        if limit > 10:
            botmsg1 = await ctx.send("You are deleting more than 10 messages. 'Y' to confirm.")
            # Wait for timeout
            try:
                msg = (await bot.wait_for('message', check=check, timeout=10.0))
            except asyncio.TimeoutError:
                await botmsg1.delete()
                await ctx.send(ctx.author.mention + "\n" + "Time is up. Delete aborted.", delete_after=5)
                return
            # Proceed to delete if user agrees
            if msg.content.lower() == "y":
                async for x in messages:
                    if deleted >= limit:
                        await ctx.send(f"{deleted} message(s) deleted.", delete_after=3)
                        break
                    await x.delete()
                    deleted += 1
                botmsg1.delete()
                msg.delete()
                return
            # Anything else will abort the delete process
            else:
                await ctx.send("Invalid command. Delete aborted.", delete_after=5)
                botmsg1.delete()
                msg.delete()
                return
        # No warning needed if argument is 10 or below
        elif limit <= 10:
            async for x in messages:
                if deleted >= limit:
                    await ctx.send(f"{deleted} message(s) deleted.", delete_after=3)
                    break
                await x.delete()
                deleted += 1


@bot.command(name='guess', description='Fun feature')
async def guess(ctx):
    await ctx.message.delete()

    def check(m):
        return m.author == ctx.author

    while True:
        botmsg1 = await ctx.send('Guess a number from 1-10: ')
        number = random.randint(1, 10)

        try:
            msg = (await bot.wait_for('message', check=check, timeout=10.0))
        except asyncio.TimeoutError:
            await botmsg1.delete()
            break
        if msg.content.lower() == "!guess":
            await botmsg1.delete()
            await msg.delete()
            break
        elif msg.content.lower() == "exit":
            await botmsg1.delete()
            await msg.delete()
            break
        if msg.content == str(number):
            botmsg2 = await ctx.send("Well you guessed it!")
            await asyncio.sleep(1)
            await botmsg1.delete()
            await botmsg2.delete()
            await msg.delete()
        else:
            botmsg2 = await ctx.send(f"NOOOO! It's {number}!!!")
            await asyncio.sleep(1)
            await botmsg1.delete()
            await botmsg2.delete()
            await msg.delete()


@bot.command(name='hi', description='mangoBot greets you')
async def greet(ctx):
    await ctx.message.delete()
    await ctx.send(greetings.greet(ctx.author.mention), delete_after=5)


@bot.command(name='quote', description='Famous Quotes')
async def quote(ctx):
    await ctx.message.delete()
    response = random.choice(quotes.quotes)
    await ctx.send(f"{ctx.author.mention} \n{response}")


# QUIZ
@bot.command(name='t', description='Trivia Quiz')
async def quiz(ctx):
    await ctx.message.delete()

    def check(m):
        return m.author == ctx.author

    while True:
        # Generate questions
        questions = triviaQuizQ
        answers = triviaQuizA
        index = random.randint(0, len(questions) - 1)
        question = questions[index]
        answer = answers[index]
        # Send question
        botmsg1 = await ctx.send(question)
        # Wait for an answer
        try:
            msg = (await bot.wait_for('message', check=check, timeout=15.0))
        except asyncio.TimeoutError:
            botmsg2 = await ctx.send(
                ctx.author.mention + "\n" + "Time is up. The correct answer is: {0}".format(answer))
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
            return
        if msg.content.lower() == answer.lower():
            botmsg2 = await ctx.send(ctx.author.mention + "\n" + "That's right!")
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
            await msg.delete()
        elif msg.content.lower() == 'exit':
            await botmsg1.delete()
            await msg.delete()
            return
        else:
            botmsg2 = await ctx.send(ctx.author.mention + "\n" + "The correct answer is: " + answer)
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
            await msg.delete()


# CLAN INFO
@bot.command(name='clan', description='Member Info.')
async def data(ctx):
    await ctx.message.delete()
    mention = str(ctx.author.mention)

    def check(m):
        return m.author == ctx.author

    # Retrieve information about clan from Clash Royale API
    key = clashToken
    base_url = "https://proxy.royaleapi.dev/v1"
    endpoint1 = "/clans/%23L2208GR9/members"
    endpoint2 = "/clans/%23L2208GR9/currentriverrace"
    request1 = requests.get(base_url + endpoint1, headers={"Authorization": "Bearer %s" % key})
    request2 = requests.get(base_url + endpoint2, headers={"Authorization": "Bearer %s" % key})
    data1 = request1.json()  # members info
    data2 = request2.json()  # war info

    bm1 = await ctx.send(f"{mention} What info are you looking for? (war/member)")
    m1 = await bot.wait_for('message', check=check)

    if m1.content.lower() == "member":
        bm2 = await ctx.send(f"{mention} Name of player?")
        m2 = await bot.wait_for('message', check=check)
        for item in data1['items']:
            if item['name'] == m2.content:
                response = f"{mention}\nName: {item['name']}\nRank: {item['role']}\nTrophies: {item['trophies']}\nArena: {item['arena']['name']}\nDonations: {item['donations']} "
                await ctx.send(response, delete_after=10)
                await bm1.delete()
                await m1.delete()
                await bm2.delete()
                await m2.delete()
                return
        await ctx.send(f"{mention} Player info not found.", delete_after=10)
        await bm1.delete()
        await m1.delete()
        await bm2.delete()
        await m2.delete()
        return

    elif m1.content.lower() == "war":
        bm2 = await ctx.send(" Name of player?")
        m2 = await bot.wait_for('message', check=check)
        for item in data2['clan']['participants']:
            if item['name'] == m2.content:
                response = "{4} \nName:{0} \nTag: {1} \nFame: {2}\nRepair points: {3}\n".format(
                    item['name'],
                    item['tag'],
                    item['fame'],
                    item['repairPoints'],
                    mention)
                await ctx.send(response, delete_after=10)
                await bm1.delete()
                await m1.delete()
                await bm2.delete()
                await m2.delete()
                return
        await ctx.send(f"{mention} Player info not found.")
        await bm1.delete()
        await m1.delete()
        await bm2.delete()
        await m2.delete()
        return

    elif m1.content == "members":
        temp = ""
        for item in data1['items']:
            temp = temp + item['name'] + ", "
        await ctx.send(f"{mention} \nThere are a total of {len(data1['items'])} members: \n{temp}", delete_after=20)
        await bm1.delete()
        await m1.delete()
        return
    else:
        await ctx.send(ctx.author.mention + "\nInvalid input, please try again from !clan.", delete_after=5)
        await bm1.delete()
        await m1.delete()
        return


# VERSUS
@bot.command(name='vs', description='Quiz PK')
async def game(ctx):
    await ctx.message.delete()
    await ctx.send(f'{ctx.author.mention} has started a pk quiz game.', delete_after=5)
    # What type of quiz?
    def check(m):
        if m.author != ctx.message.author and m.author == bot.user:
            return False
        try:
            quizChoice = int(m.content)
            if quizChoice not in range(1, 4):
                return False
        except ValueError:
            return False
        return True

    bm1 = await ctx.send(f"{ctx.author.mention} What type of quiz?\n (1) Management \n (2) Math \n (3) Trivia")
    try:
        e = await bot.wait_for('message', check=check, timeout=15)
        if int(e.content) == 1:
            await ctx.send('{} has selected {} Quiz'.format(ctx.author.mention, 'management'), delete_after=5)
            gameType = 'management'
        elif int(e.content) == 2:
            await ctx.send('{} has selected {} Quiz'.format(ctx.author.mention, 'math'), delete_after=5)
            gameType = 'math'
        elif int(e.content) == 3:
            await ctx.send('{} has selected {} Quiz'.format(ctx.author.mention, 'trivia'), delete_after=5)
            gameType = 'trivia'
        await bm1.delete()
        await e.delete()
    except asyncio.TimeoutError:
        await ctx.send("Timeout. Game Over.", delete_after=5)
        await bm1.delete()
        return

    # How many questions?
    def check(m):
        if m.author != ctx.message.author and m.author == bot.user:
            return False
        try:
            nGames = int(m.content)
        except ValueError:
            return False
        if nGames <= 0:
            return False
        return True

    bm1 = await ctx.send("{}, how many questions are we playing?".format(ctx.author.mention))
    try:
        m1 = await bot.wait_for('message', check=check, timeout=15)
        games = int(m1.content)
        await bm1.delete()
        await m1.delete()
    except asyncio.TimeoutError:
        bm1.delete()
        await ctx.send('Timeout. Game Over.', delete_after=5)
        return

    # Player X please enter your name
    class Player:
        def __init__(self, score, name, userid):
            self.score = score
            self.name = name
            self.id = userid

        def win(self):
            self.score += 1

        def lose(self):
            self.score -= 1

        def info(self):
            return f"Name: {self.name}\nScore: {self.score}"

    playerList = []

    def check(m):
        if m.author == bot.user:
            return False
        for player in playerList:
            if player.id == m.author:
                return False
        return True

    i = 1
    while True:
        bm1 = await ctx.send('Player {} Enter Your Name. Game begins in 15s.'.format(i))
        try:
            e = await bot.wait_for('message', check=check, timeout=15)
            playerList.append(Player(0, e.content, e.author))
            await bm1.delete()
            await e.delete()
            i += 1
        except asyncio.TimeoutError:
            if len(playerList) == 0:
                await bm1.delete()
                await ctx.send('No players. Game Over.', delete_after=5)
                return
            await bm1.delete()
            break

    # Get quiz questions set based on type of quiz
    if gameType == 'trivia':
        questions = triviaQuizQ
        answers = triviaQuizA
    elif gameType == 'management':
        questions = managementQuizQ
        answers = managementQuizA

    # Loop for number of rounds of game
    for x in range(games):
        score_msg_array = []
        for i in range(len(playerList)):
            score_msg_array.append(await ctx.send(playerList[i].info()))

        # Get questions from quiz set
        if gameType == 'trivia' or gameType == 'management':
            index = random.randint(0, len(questions) - 1)
            question = questions[index]
            answer = answers[index]

        # Generate math questions
        elif gameType == 'math':
            a = random.randint(1, 99)
            b = random.randint(50, 99)
            c = random.randint(1, 5)
            d = random.randint(1, 5)
            question = f"{a} x ({c}+{d}) + {b} = ?"
            answer = str(a * (c + d) + b)

        waitmsg = await ctx.send('Question coming up in 5.....')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 4....')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 3...')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 2..')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 1.')
        await asyncio.sleep(1)
        await waitmsg.delete()
        botmsg1 = await ctx.send(question)

        def check(m):
            for player in playerList:
                if m.author == player.id:
                    return True
            return False
        try:
            msg = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            botmsg2 = await ctx.send("Time is up. The correct answer is: " + answer)
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
        else:
            if msg.content.lower() == "exit":
                await botmsg1.delete()
                await msg.delete()
                return
            elif msg.content.lower() == answer.lower():
                botmsg2 = await ctx.send(msg.author.mention + "\n" + "That's right!")
                for player in playerList:
                    if msg.author == player.id:
                        player.win()
                        break
                await asyncio.sleep(5)
                await botmsg1.delete()
                await botmsg2.delete()
                await msg.delete()
            else:
                botmsg2 = await ctx.send("\n" + "The correct answer is: " + answer)
                for player in playerList:
                    if msg.author == player.id:
                        player.lose()
                        break
                await asyncio.sleep(5)
                await botmsg1.delete()
                await botmsg2.delete()
                await msg.delete()

        for score in score_msg_array:
            await score.delete()

    botmsg1 = await ctx.send("Good game and well played! Here are the scores:")
    score_msg_array = []
    for i in range(len(playerList)):
        score_msg_array.append(await ctx.send(playerList[i].info()))
    await asyncio.sleep(10)
    await botmsg1.delete()
    for score in score_msg_array:
        await score.delete()


# ==================================================================================================================== #
bot.run(discordToken)
