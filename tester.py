# tester.py
import random
import os
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import asyncio
import requests
from youtubesearchpython import searchYoutube
import ast


vname = "mangoBot tester"

# ==================================================================================================================== #
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='test')
async def game(ctx, a: int):
    class player():
        def __init__(self, score, name, id):
            self.score = score
            self.name = name
            self.id = id

        def win(self):
            self.score += 1

        def lose(self):
            self.score -= 1

        def info(self):
            return f"Name:   {self.name}\nScore:   {self.score}"

    def check1(m):
        return m.author != msg1.author

    botmsg1 = (await ctx.send("Player 1 Please Type in Your Name."))
    msg1 = (await bot.wait_for('message'))
    botmsg2 = (await ctx.send("Player 2 Please Type in Your Name."))
    msg2 = (await bot.wait_for('message', check=check1))
    #botmsg3 = (await ctx.send("Player 3 Please Type in Your Name."))
    #msg3 = (await bot.wait_for('message'))
    #botmsg4 = (await ctx.send("Player 4 Please Type in Your Name."))
    #msg4 = (await bot.wait_for('message'))

    await botmsg1.delete()
    await botmsg2.delete()
    await msg1.delete()
    await msg2.delete()
    #await botmsg3.delete()
    #await botmsg4.delete()
    #await msg3.delete()
    #await msg4.delete()

    p1 = player(0, msg1.content, msg1.author)
    p2 = player(0, msg2.content, msg2.author)
    #p3 = player(0, msg3.content, msg3.author)
    #p4 = player(0, msg4.content, msg4.author)

    await ctx.send(p1.info())
    await ctx.send(p2.info())
    #await ctx.send(p3.info())
    #await ctx.send(p4.info())

    import quiz
    questions = quiz.quizset
    answers = quiz.answers

    for x in range(a):

        score1 = await ctx.send(p1.info())
        score2 = await ctx.send(p2.info())
        #score3 = await ctx.send(p3.info())
        #score4 = await ctx.send(p4.info())

        index = random.randint(0, len(questions) - 1)
        question = questions[index]
        answer = answers[index]
        botmsg1 = await ctx.send(question)


        def check2(m):
            a = m.author == p1.id
            b = m.author == p2.id
            #c = m.author == p3.id
            #d = m.author == p4.id
            e = a or b
            return m.author != bot.user and e

        try:
            msg = (await bot.wait_for('message', check=check2, timeout=15.0))
        except asyncio.TimeoutError:
            botmsg2 = await ctx.send("Time is up. The correct answer is: {0}".format(answer))
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
            return
        if msg.content.lower() == answer.lower():
            botmsg2 = await ctx.send(msg.author.mention + "\n" + "That's right!")
            if msg.author == p1.id:
                p1.win()
            elif msg.author == p2.id:
                p2.win()
            #elif msg.author == p3.id:
                #p3.win()
            #elif msg.author == p4.id:
                #p4.win()

            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
            await msg.delete()
        else:
            botmsg2 = await ctx.send(msg.author.mention + "\n" + "The correct answer is: " + answer)
            if msg.author == p1.id:
                p1.lose()
            elif msg.author == p2.id:
                p2.lose()
            #elif msg.author == p3.id:
                #p3.lose()
            #elif msg.author == p4.id:
                #p4.lose()
            await asyncio.sleep(5)
            await botmsg1.delete()
            await botmsg2.delete()
            await msg.delete()

        await score1.delete()
        await score2.delete()
        #await score3.delete()
        #await score4.delete()

    await ctx.send("Good game and well played. Here are the scores:")
    await ctx.send(p1.info())
    await ctx.send(p2.info())
    #await ctx.send(p3.info())
    #await ctx.send(p4.info())



@bot.command(name='u', help='mangoBot searches youtube and returns top search.')
async def test(ctx):
    def check(m):
        return m.author == ctx.author

    await ctx.send("Your search?")
    msg = (await bot.wait_for('message', check=check))
    query = msg.content
    search = (searchYoutube(query, offset=1, mode="json", max_results=1)).result()
    url = ast.literal_eval(search)
    await ctx.send(url['search_result'][0]['link'])


@bot.command(name='ver', help='Shows current version of mangoBot')
async def version(ctx):
    botmsg = await ctx.send("Current Build: " + vname)
    await asyncio.sleep(5)
    await botmsg.delete()
    await ctx.message.delete()


@bot.command(name='c', help='mangoBot deletes your messages. Specify number of messages to delete.')
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
            limit = int(args[0])
        except ValueError:
            botmsg = await ctx.send("Invalid. Careful, !c is a delete command.")
            await asyncio.sleep(5)
            await botmsg.delete()
            return

        if int(args[0]) > 10:
            botmsg1 = await ctx.send("You are deleting more than 10 messages. 'Y' to confirm.")

            def check(m):
                return m.author == ctx.author

            try:
                msg = (await bot.wait_for('message', check=check, timeout=10.0))
            except asyncio.TimeoutError:
                botmsg2 = await ctx.send(ctx.author.mention + "\n" + "Time is up. Delete aborted.")
                await asyncio.sleep(5)
                await botmsg1.delete()
                await botmsg2.delete()
                return
            if msg.content == "Y":
                await ctx.message.delete()
                messages = ctx.channel.history().filter(lambda m: m.author == ctx.author)
                limit = int(args[0]) + 1
                i = 1
                async for x in messages:
                    if i <= limit:
                        await x.delete()
                    else:
                        print("Messages deleted:", i - 2)
                        break
                    i += 1
                botmsg2 = await ctx.send(str(limit-1) + " of your messages are deleted.")
                await asyncio.sleep(5)
                await msg.delete()
                await botmsg1.delete()
                await botmsg2.delete()
            else:
                await ctx.send("Invalid command. Delete aborted.")
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


@bot.command(name='guess', help='just a fun feature. Tee Hee.')
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


@bot.command(name='hi', help='mangoBot greets you.')
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


@bot.command(name='time', help='mangoBot tells you the current time.')
async def time(ctx):
    now = datetime.now(timezone('Asia/Singapore'))
    response = now.strftime("%H:%M\n%d %B %Y")
    botmsg = await ctx.send(ctx.author.mention + "\n" + response)
    await asyncio.sleep(5)
    await botmsg.delete()
    await ctx.message.delete()


@bot.command(name='quote', help='mangoBot sends you a quote.')
async def quote(ctx):
    import quotes
    response = random.choice(quotes.quotes)
    await ctx.message.delete()
    await ctx.send(ctx.author.mention + "\n" + response)


@bot.command(name='quiz', help='mangoBot sends you a trivia quiz question.')
async def quiz(ctx):
    import quiz
    questions = quiz.quizset
    answers = quiz.answers
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


@bot.command(name='clan', help='Retrieve member information. Follow the questions of mangoBot accordingly.')
async def data(ctx):
    key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
          ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc2YWYzMGJmLWFjYzgtNGE0Ny1" \
          "hZmU2LWIwZjE0NzY2ZWNlYyIsImlhdCI6MTU5MjMxMzY0OSwic3ViIjoiZGV2ZWxvcGVyL2JjNzVkYTRmLTEyMGItOWU3Ny0" \
          "xMTA0LWM0YmQxMDllMDc5OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZ" \
          "lciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0" \
          ".czFtTMv7pqaziRUiivFYyXdvwAvPQNpI7w9tNvrExj0cvzYFl20GHtdLL3LiVKM-ZUFs1wTXeSqfjXgygssT2g "

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
        botmsg2 = await ctx.send(ctx.author.mention + f"\nThere are a total of {len(data1['items'])} members. \nAs requested, "
                                            f"this is the list of clan members:\n\n" + temp)
        await ctx.message.delete()
        await botmsg1.delete()
        await msg1.delete()
        await asyncio.sleep(10)
        await botmsg2.delete()
    else:
        botmsg2 = await ctx.send(ctx.author.mention + "\nInvalid input, please try again from !clan-info.")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await botmsg1.delete()
        await msg1.delete()
        await botmsg2.delete()
# ==================================================================================================================== #
bot.run('NzI1Nzg1OTQ4MDgzNzE2MTI2.XvjCHg.2Eixr_ZjK1nvEXlZKH-vMnIpOHY')
