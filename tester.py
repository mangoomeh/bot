# tester.py
import random
import os
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import asyncio
import requests


vname = "mangoBot tester"

# ==================================================================================================================== #
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='test')
async def test(ctx):
    msg = await ctx.send("This should be deleted.")
    await asyncio.sleep(5)
    await msg.delete()


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
            msg = await ctx.send("Invalid. Careful, !c is a delete command.")
            await asyncio.sleep(5)
            await msg.delete()
            return

        if int(args[0]) > 10:
            msg1 = await ctx.send("You are deleting more than 10 messages. 'Y' to confirm.")

            def check(m):
                return m.author == ctx.author

            try:
                msg = (await bot.wait_for('message', check=check, timeout=10.0)).content
            except asyncio.TimeoutError:
                msg = await ctx.send(ctx.author.mention + "\n" + "Time is up. Delete aborted.")
                await asyncio.sleep(5)
                await msg1.delete()
                await msg.delete()
                return
            if msg == "Y":
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
                msg2 = await ctx.send(str(limit-1) + " of your messages are deleted.")
                await asyncio.sleep(5)
                await msg1.delete()
                await msg2.delete()
            else:
                await ctx.send("Invalid command.")
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
    await ctx.send('Guess a number from 1-10: ')
    number = random.randint(1, 10)
    print(number)

    def check(m):
        return m.author == ctx.author

    msg = (await bot.wait_for('message', check=check)).content.lower()
    if msg == "!guess":
        return
    if msg == str(number):
        await ctx.send("Well you guessed it!")
    else:
        await ctx.send(f"NOOOO! It's {number}!!!")


@bot.command(name='ver', help='Shows current version of mangoBot')
async def version(ctx):
    name = ctx.author
    name = str(name)
    print(name[:-5])
    await ctx.send("Current Build: " + vname)


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
    await ctx.send(response)

    def check(m):
        return m.author == ctx.author

    await bot.wait_for('message', check=check)
    import textfaces
    response = random.choice(textfaces.textfaces)
    await ctx.send(response)


@bot.command(name='time', help='mangoBot tells you the current time.')
async def time(ctx):
    now = datetime.now(timezone('Asia/Singapore'))
    response = now.strftime("%H:%M\n%d %B %Y")
    await ctx.send(ctx.author.mention + "\n" + response)


@bot.command(name='quote', help='mangoBot sends you a quote.')
async def quote(ctx):
    import quotes
    response = random.choice(quotes.quotes)
    await ctx.send(ctx.author.mention + "\n" + response)


@bot.command(name='quiz', help='mangoBot sends you a trivia quiz question.')
async def quiz(ctx):
    import quiz
    questions = quiz.quizset
    answers = quiz.answers
    index = random.randint(0, len(questions) - 1)
    question = questions[index]
    answer = answers[index]
    await ctx.send(question)

    def check(m):
        return m.author == ctx.author

    try:
        msg = (await bot.wait_for('message', check=check, timeout=15.0)).content.lower()
    except asyncio.TimeoutError:
        await ctx.send(ctx.author.mention + "\n" + "Time is up. The correct answer is: {0}".format(answer))
        return
    if msg == answer.lower():
        await ctx.send(ctx.author.mention + "\n" + "That's right!")
    else:
        await ctx.send(ctx.author.mention + "\n" + "The correct answer is: " + answer)


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

    await ctx.send(ctx.author.mention + "\nWhat info are you looking for? (war/member)")

    def check(m):
        return m.author == ctx.author

    msg = (await bot.wait_for('message', check=check)).content.lower()
    if msg == "member":
        await ctx.send(ctx.author.mention + " Name of player?")
        msg = (await bot.wait_for('message', check=check)).content
        for item in data1['items']:
            x = item['name'] == msg
            if x:
                response1 = "Name: {0} \nRank: {1} \nTrophies: {2} \nArena: {3} \nDonations: {4} \n".format(
                    item['name'],
                    item['role'],
                    item["trophies"],
                    item['arena']['name'],
                    item["donations"])
                await ctx.send(ctx.author.mention + "\n" + response1)
                break
        if not x:
            await ctx.send(ctx.author.mention + "\nPlayer info not found.")
    elif msg == "war":
        if data2['state'] == "notInWar":
            await ctx.send(ctx.author.mention + "\nWe are currently not in war.")
            return
        await ctx.send(" Name of player?")
        msg = (await bot.wait_for('message', check=check)).content
        for item in data2['participants']:
            x = item['name'] == msg
            if x:
                response2 = "Name:{0} \nCollection Day: {1}/3 \nBattles Played: {2}/{3} \nWins: {4}/{2} \n".format(
                    item['name'],
                    item['collectionDayBattlesPlayed'],
                    item["battlesPlayed"],
                    item['numberOfBattles'],
                    item['wins'])
                await ctx.send(ctx.author.mention + "\n" + response2)
                break
        if not x:
            await ctx.send(ctx.author.mention + "\nPlayer info not found.")
    elif msg == "members":
        temp = ""
        for item in data1['items']:
            temp = temp + item['name'] + "\n"
        await ctx.send(ctx.author.mention + f"\nThere are a total of {len(data1['items'])} members. \nAs requested, "
                                            f"this is the list of clan members:\n\n" + temp)
    else:
        await ctx.send(ctx.author.mention + "\nInvalid input, please try again from !clan-info.")
# ==================================================================================================================== #
bot.run('NzI1Nzg1OTQ4MDgzNzE2MTI2.XvjCHg.2Eixr_ZjK1nvEXlZKH-vMnIpOHY')
