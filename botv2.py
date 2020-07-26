# botv2.py
import random
import os
import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import asyncio
import requests
import ast
from youtubesearchpython import searchYoutube
import logging
import tester
import profanities

logging.basicConfig(format='%(asctime)s : %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

vname = "mangoBot v4.0"

# ==================================================================================================================== #
me = "Only usable by mangoomeh"
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


def owner(m):
    return m.author.id == 311159834823360512


def dev(m):
    a = 334645578111647746
    b = 311159834823360512
    c = 372024452042457108
    return m.author.id == a or m.author.id == b or m.author.id == c


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    mm = message.content

    for i in profanities.profanities:
        if i in mm.lower():
            logging.info(str(mm))
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please mind your language :)", delete_after=3)
            return

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


@bot.command(name='test', description=me)
@commands.check(owner)
async def test():
    pass


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


@bot.command(name='zc', description="developers only")
@commands.check(dev)
async def overclear(ctx):
    def check(m):
        return m.author == ctx.author
    await ctx.message.delete()
    members = ctx.channel.members
    botmsg = "Whose messages are we deleting?\n\n"
    for i in range(len(members)):
        line = f"({i + 1}) {members[i].name}: {members[i].id}\n"
        botmsg += line
    botmsg = await ctx.send(botmsg)
    msg = await bot.wait_for('message', check=check)
    await botmsg.delete()
    await msg.delete()
    if msg.content.lower() == "cancel":
        return
    elif msg.content.lower() == "all":
        messages = ctx.channel.history()
        botmsg = await ctx.send('How many messages?')
        msg = await bot.wait_for('message', check=check)
        limit = int(msg.content)
        await botmsg.delete()
        await msg.delete()
        i = 1
        async for x in messages:
            if i <= limit:
                await x.delete()
            else:
                break
            i += 1
        await ctx.send(f"{limit} message(s) deleted.", delete_after=3)
    else:
        index = int(msg.content) - 1
        messages = ctx.channel.history().filter(lambda m: m.author.id == members[index].id)
        botmsg = await ctx.send('How many messages?')
        msg = await bot.wait_for('message', check=check)
        limit = int(msg.content)
        await botmsg.delete()
        await msg.delete()
        i = 1
        async for x in messages:
            if i <= limit:
                await x.delete()
            else:
                break
            i += 1
        await ctx.send(f"{limit} message(s) deleted.", delete_after=3)


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


@bot.command(name='zclear', description=me)
@commands.check(owner)
async def mangoclear(ctx, a: int):
    await ctx.message.delete()
    messages = ctx.channel.history().filter(lambda m: m.author == bot.user)
    limit = a
    i = 1
    async for x in messages:
        if i <= limit:
            await x.delete()
        else:
            break
        i += 1
    botmsg = await ctx.send(f"{limit} message(s) deleted.")
    await asyncio.sleep(3)
    await botmsg.delete()


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
    await ctx.send(helptext, delete_after=10)


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
    while True:
        a = random.randint(1, 99)
        b = random.randint(50, 99)
        c = random.randint(1, 5)
        d = random.randint(1, 5)
        question = f"{a} x ({c}+{d}) + {b} = ?"
        answer = str(a * (c + d) + b)
        botmsg1 = await ctx.send(question)
        try:
            def check(m):
                return m.author == ctx.message.author

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
        msg = (await bot.wait_for('message', check=check, timeout=30))
    except asyncio.TimeoutError:
        botmsg2 = (await ctx.send("Timeout. Try again at !u."))
        await asyncio.sleep(5)
        await botmsg.delete()
        await botmsg2.delete()
        return

    query = msg.content
    search = (searchYoutube(query, offset=1, mode="json", max_results=max_results)).result()
    search_results = ast.literal_eval(search)
    await botmsg.delete()
    await msg.delete()
    botmsg = ""
    link_array = []
    for i in range(max_results):
        title = search_results['search_result'][i]['title']
        title = str(title)
        duration = search_results['search_result'][i]['duration']
        link = search_results['search_result'][i]['link']
        botmsg += f"({i + 1}) {title} [{duration}]\n"
        link_array.append(link)

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
        await ctx.send(link_array[index - 1])


@bot.command(name='c', description='Delete message')
async def clear(ctx, *args):
    if len(args) == 0:
        await ctx.message.delete()
        messages = ctx.channel.history().filter(lambda m: m.author == ctx.author)
        limit = 1
        i = 1
        async for x in messages:
            if i <= limit:
                await x.delete()
            else:
                print("Messages deleted:", i - 1)
                break
            i += 1
    else:
        try:
            int(args[0])
        except ValueError:
            botmsg = await ctx.send("Invalid. Careful, !c is a delete command.")
            await asyncio.sleep(5)
            await botmsg.delete()
            return

        if int(args[0]) > 10:
            messages = ctx.channel.history().filter(lambda m: m.author == ctx.author)
            botmsg1 = await ctx.send("You are deleting more than 10 messages. 'Y' to confirm.")

            def check(m):
                return m.author == ctx.author

            try:
                msg = (await bot.wait_for('message', check=check, timeout=10.0))
                await botmsg1.delete()
            except asyncio.TimeoutError:
                await botmsg1.delete()
                await ctx.send(ctx.author.mention + "\n" + "Time is up. Delete aborted.", delete_after=5)
                return
            if msg.content == "Y":
                await ctx.message.delete()
                limit = int(args[0]) + 1  # +1 TO INCLUDE THE MESSAGE "Y"
                i = 1
                async for x in messages:
                    if i <= limit:
                        await x.delete()
                    else:
                        print("Messages deleted:", i - 2)
                        break
                    i += 1
                await ctx.send(f"{i} of your messages are deleted.", delete_after=5)
                return
            else:
                await ctx.send("Invalid command. Delete aborted.", delete_after=5)
                return
        else:
            await ctx.message.delete()
            messages = ctx.channel.history().filter(lambda m: m.author == ctx.author)
            limit = int(args[0])
            i = 1
            async for x in messages:
                if i <= limit:
                    await x.delete()
                else:
                    print("Messages deleted:", i - 1)
                    break
                i += 1


@bot.command(name='guess', description='Fun feature')
async def guess(ctx):
    await ctx.message.delete()
    while True:
        botmsg1 = await ctx.send('Guess a number from 1-10: ')
        number = random.randint(1, 10)

        def check(m):
            return m.author == ctx.author

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
    greetings = [
        f"Hi {ctx.author.mention}, I'm mangoBot!",
        f"Hello {ctx.author.mention}, I love mango~",
        f"{ctx.author.mention} at your service.",
        f"Good day {ctx.author.mention}~",
        f"{ctx.author.mention} Nice to meet you!",
        f"{ctx.author.mention} How are you doing?",
        f"{ctx.author.mention} What's up?",
        f"{ctx.author.mention} Do you know that you can access my list of commands using !help ?",
        f"Zzz...(what?) oh sorry {ctx.author.mention} I was just snoozing a lil.",
        f"{ctx.author.mention} why are you talking to a bot? Haha, just kidding.",
        f"{ctx.author.mention} Sorry what did you say again?",
        f"{ctx.author.mention} Hi there!",
        f"{ctx.author.mention} Heeeeeeyyyyyy~",
        f"{ctx.author.mention} Whatcha doin'?",
        f"Hi {str(ctx.author)[:-5]}",
        f"{str(ctx.author)[:-5]} is talking to mangoBot~",
        f"mangoBot wants to talk to {str(ctx.author)[:-5]}",
        f"{str(ctx.author)[:-5]} wanna test how knowledgeable you are? Try using !quiz !",
        f"{str(ctx.author)[:-5]}, get a quote from me by using !quote :)",
        f"{str(ctx.author)[:-5]}, do you you can check time using !time ?"
    ]
    response = random.choice(greetings)
    botmsg1 = await ctx.send(response)

    def check(m):
        return m.author == ctx.author

    try:
        msg = await bot.wait_for('message', check=check, timeout=5)
    except asyncio.TimeoutError:
        botmsg2 = await ctx.send(f'{ctx.author.mention} bye~')
        await botmsg1.delete()
        await ctx.message.delete()
        await asyncio.sleep(3)
        await botmsg2.delete()

        return
    if msg.content == "!hi":
        await asyncio.sleep(5)
        await botmsg1.delete()
        await ctx.message.delete()
        await msg.delete()
        return
    else:
        import textfaces
        response = random.choice(textfaces.textfaces)
        botmsg2 = await ctx.send(response)
        await asyncio.sleep(5)
        await botmsg1.delete()
        await botmsg2.delete()
        await ctx.message.delete()
        await msg.delete()


@bot.command(name='quote', description='Famous Quotes')
async def quote(ctx):
    import quotes
    response = random.choice(quotes.quotes)
    await ctx.message.delete()
    await ctx.send(ctx.author.mention + "\n" + response)


# QUIZ
@bot.command(name='t', description='Trivia Quiz')
async def quiz(ctx):
    import quiz
    questions = quiz.trivia_quiz_set
    answers = quiz.trivia_answers
    index = random.randint(0, len(questions) - 1)
    question = questions[index]
    answer = answers[index]
    botmsg1 = await ctx.send(question)

    def check(m):
        return m.author == ctx.author

    try:
        msg = (await bot.wait_for('message', check=check, timeout=15.0))
    except asyncio.TimeoutError:
        botmsg2 = await ctx.send(ctx.author.mention + "\n" + "Time is up. The correct answer is: {0}".format(answer))
        await asyncio.sleep(5)
        await botmsg1.delete()
        await botmsg2.delete()
        await ctx.message.delete()
        return
    if msg.content.lower() == answer.lower():
        botmsg2 = await ctx.send(ctx.author.mention + "\n" + "That's right!")
        await asyncio.sleep(5)
        await botmsg1.delete()
        await botmsg2.delete()
        await msg.delete()
        await ctx.message.delete()
    else:
        botmsg2 = await ctx.send(ctx.author.mention + "\n" + "The correct answer is: " + answer)
        await asyncio.sleep(5)
        await botmsg1.delete()
        await botmsg2.delete()
        await msg.delete()
        await ctx.message.delete()


# CLAN INFO
@bot.command(name='clan', description='Member Info.')
async def data(ctx):
    key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
          ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc2YWYzMGJmLWFjYzgtNGE0Ny1" \
          "hZmU2LWIwZjE0NzY2ZWNlYyIsImlhdCI6MTU5MjMxMzY0OSwic3ViIjoiZGV2ZWxvcGVyL2JjNzVkYTRmLTEyMGItOWU3Ny0" \
          "xMTA0LWM0YmQxMDllMDc5OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZ" \
          "lciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0" \
          ".czFtTMv7pqaziRUiivFYyXdvwAvPQNpI7w9tNvrExj0cvzYFl20GHtdLL3LiVKM-ZUFs1wTXeSqfjXgygssT2g"

    base_url = "https://proxy.royaleapi.dev/v1"

    endpoint1 = "/clans/%23L2208GR9/members"
    endpoint2 = "/clans/%23L2208GR9/currentwar"

    request1 = requests.get(base_url + endpoint1, headers={"Authorization": "Bearer %s" % key})
    request2 = requests.get(base_url + endpoint2, headers={"Authorization": "Bearer %s" % key})

    data1 = request1.json()
    data2 = request2.json()

    botmsg1 = await ctx.send(ctx.author.mention + "\nWhat info are you looking for? (war/member)")

    def check(m):
        return m.author == ctx.author

    msg1 = (await bot.wait_for('message', check=check))
    if msg1.content.lower() == "member":
        botmsg2 = await ctx.send(ctx.author.mention + " Name of player?")
        msg2 = (await bot.wait_for('message', check=check))
        x = False
        for item in data1['items']:
            x = item['name'] == msg2.content
            if x:
                response1 = "Name: {0} \nRank: {1} \nTrophies: {2} \nArena: {3} \nDonations: {4} \n".format(
                    item['name'],
                    item['role'],
                    item["trophies"],
                    item['arena']['name'],
                    item["donations"])
                botmsg3 = await ctx.send(ctx.author.mention + "\n" + response1)
                await ctx.message.delete()
                await botmsg1.delete()
                await msg1.delete()
                await botmsg2.delete()
                await msg2.delete()
                await asyncio.sleep(10)
                await botmsg3.delete()
                break
        if not x:
            botmsg3 = await ctx.send(ctx.author.mention + "\nPlayer info not found.")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await botmsg1.delete()
            await msg1.delete()
            await botmsg2.delete()
            await msg2.delete()
            await botmsg3.delete()
    elif msg1.content.lower() == "war":
        if data2['state'] == "notInWar":
            botmsg2 = await ctx.send(ctx.author.mention + "\nWe are currently not in war.")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await botmsg1.delete()
            await msg1.delete()
            await botmsg2.delete()
            return
        botmsg2 = await ctx.send(" Name of player?")
        msg2 = (await bot.wait_for('message', check=check))
        x = False
        for item in data2['participants']:
            x = item['name'] == msg2.content
            if x:
                response2 = "Name:{0} \nCollection Day: {1}/3 \nBattles Played: {2}/{3} \nWins: {4}/{2} \n".format(
                    item['name'],
                    item['collectionDayBattlesPlayed'],
                    item["battlesPlayed"],
                    item['numberOfBattles'],
                    item['wins'])
                botmsg3 = await ctx.send(ctx.author.mention + "\n" + response2)
                await ctx.message.delete()
                await botmsg1.delete()
                await msg1.delete()
                await botmsg2.delete()
                await msg2.delete()
                await asyncio.sleep(10)
                await botmsg3.delete()
                break
        if not x:
            botmsg3 = await ctx.send(ctx.author.mention + "\nPlayer info not found.")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await botmsg1.delete()
            await msg1.delete()
            await botmsg2.delete()
            await msg2.delete()
            await botmsg3.delete()
    elif msg1.content == "members":
        temp = ""
        for item in data1['items']:
            temp = temp + item['name'] + ", "
        botmsg2 = await ctx.send(
            ctx.author.mention + f"\nThere are a total of {len(data1['items'])} members. \nAs requested, "
                                 f"this is the list of clan members:\n\n" + temp)
        await ctx.message.delete()
        await botmsg1.delete()
        await msg1.delete()
        await asyncio.sleep(10)
        await botmsg2.delete()
    else:
        botmsg2 = await ctx.send(ctx.author.mention + "\nInvalid input, please try again from !clan.")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await botmsg1.delete()
        await msg1.delete()
        await botmsg2.delete()


# VERSUS
@bot.command(name='vs', description='Quiz PK')
async def game(ctx):
    await ctx.message.delete()

    # Check if message is from command author
    def check(m):
        return m.author == ctx.message.author

    # What type of quiz?
    botmsg1 = await ctx.send("What type of quiz? (management/math/trivia)")
    try:
        while True:
            msg1 = await bot.wait_for('message', check=check, timeout=15)
            game_type = msg1.content.lower()
            if game_type != 'management' and game_type != 'math' and game_type != 'trivia':
                await msg1.delete()
                await botmsg1.edit(content='No such type. Please enter either management, math or trivia.')
            else:
                break
    except asyncio.TimeoutError:
        botmsg2 = await ctx.send("Timeout.")
        await asyncio.sleep(3)
        await botmsg1.delete()
        await botmsg2.delete()
        return
    await botmsg1.delete()
    await msg1.delete()

    # Check if reply is a non-zero integer value and message is from command author
    def checkint(m):
        try:
            a = int(m.content) != 0
        except ValueError:
            return False
        return a and m.author == ctx.message.author

    # How many players?
    botmsg1 = await ctx.send("How many players?")
    try:
        msg1 = await bot.wait_for('message', check=checkint, timeout=15)
        players = int(msg1.content)
        await botmsg1.delete()
        await msg1.delete()
    except asyncio.TimeoutError:
        botmsg2 = await ctx.send("Timeout.")
        await asyncio.sleep(3)
        await botmsg1.delete()
        await botmsg2.delete()
        return

    # How many rounds?
    botmsg1 = await ctx.send("How many rounds are we playing?")
    try:
        msg1 = await bot.wait_for('message', check=checkint, timeout=15)
        games = int(msg1.content)
        await botmsg1.delete()
        await msg1.delete()
    except asyncio.TimeoutError:
        botmsg2 = await ctx.send('Timeout.')
        await asyncio.sleep(3)
        await botmsg1.delete()
        await botmsg2.delete()
        return

    # Generate Player Classes
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
            return f"Name:   {self.name}\nScore:   {self.score}"

    # Generate list of Players
    player_array = []
    for i in range(players):

        def check(m):
            for player in player_array:
                b = m.author != player.id
                if not b:
                    return False
            return m.author != bot.user

        botmsg = await ctx.send(f"Player {i + 1} Please Enter Your Name.")
        try:
            msg = await bot.wait_for('message', check=check, timeout=15)
            await msg.delete()
            player_array.append(Player(0, msg.content, msg.author))
        except asyncio.TimeoutError:
            pass
        await botmsg.delete()

    # Check if there are any Players
    if len(player_array) == 0:
        botmsg = await ctx.send('No players. Game aborted.')
        await asyncio.sleep(3)
        await botmsg.delete()
        return

    # Get quiz questions set based on type of quiz
    import quiz
    if game_type == 'trivia':
        questions = quiz.trivia_quiz_set
        answers = quiz.trivia_answers
    elif game_type == 'management':
        questions = quiz.management_quiz_set
        answers = quiz.management_answers
    elif game_type == 'math':
        pass
    else:
        botmsg = await ctx.send('No such type of quiz.')
        await asyncio.sleep(3)
        await botmsg.delete()
        return

    # Loop for number of rounds of game
    for x in range(games):
        score_msg_array = []
        for i in range(len(player_array)):
            score_msg_array.append(await ctx.send(player_array[i].info()))

        # Get questions from quiz set
        if game_type == 'trivia' or game_type == 'management':
            index = random.randint(0, len(questions) - 1)
            question = questions[index]
            answer = answers[index]

        # Generate math questions
        elif game_type == 'math':
            a = random.randint(1, 99)
            b = random.randint(50, 99)
            c = random.randint(1, 5)
            d = random.randint(1, 5)
            question = f"{a} x ({c}+{d}) + {b} = ?"
            answer = str(a * (c + d) + b)

        waitmsg = await ctx.send('Question coming up in 5...')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 4..')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 3...')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 2..')
        await asyncio.sleep(1)
        await waitmsg.edit(content='Question coming up in 1...')
        await asyncio.sleep(1)
        await waitmsg.delete()
        botmsg1 = await ctx.send(question)

        try:
            def check(m):
                for player in player_array:
                    a = m.author == player.id
                    if a:
                        return a
                return False

            msg = (await bot.wait_for('message', check=check, timeout=15.0))
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
                for player in player_array:
                    if msg.author == player.id:
                        player.win()
                        break
                await asyncio.sleep(5)
                await botmsg1.delete()
                await botmsg2.delete()
                await msg.delete()
            else:
                botmsg2 = await ctx.send("\n" + "The correct answer is: " + answer)
                for player in player_array:
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
    for i in range(len(player_array)):
        score_msg_array.append(await ctx.send(player_array[i].info()))
    await asyncio.sleep(10)
    await botmsg1.delete()
    for score in score_msg_array:
        await score.delete()


# ==================================================================================================================== #

bot.run(os.environ['token'])
# bot.run(tester.token)
