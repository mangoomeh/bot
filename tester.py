import discord
import random
import asyncio
import requests

client = discord.Client()


# ===================================================== #
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds)
    print('We have logged in as {0.user}'.format(client))
    print('We are connected to {0}'.format(guild))


@client.event
async def on_message(message):
    if message.author == client.user or message.content.startswith('!') is not True:
        return
    args = message.content.split(' ')
    command = args[0][1:]
    channel = message.channel
    greetings = [
        f"Hi {message.author.mention}, I'm mangoBot!",
        f"Hello {message.author.mention}, I love mango~",
        f"{message.author.mention} at your service.",
        f"Good day {message.author.mention}~",
        f"{message.author.mention} Nice to meet you!",
        f"{message.author.mention} How are you doing?"
    ]

    quotes = [
        'In every day, there are 1,440 minutes. That means we have 1,440 daily opportunities to make a positive '
        'impact. \n-Les Brown',
        'Positive anything is better than negative nothing. \n-Elbert Hubbard',
        "Be thankful or everything that happens in your life; it's all an experience. \n-Bennett",
        "It's not whether you get knocked down, it's whether you get up. \n-Lombardi",
        "The happiness of your life depends upon the quality of your thoughts. \n-Aurelius",
        "Keep your face to the sunshine and you cannot see the shadow. \n-Helen Keller",
        "Happiness is an attitude. We either make ourselves miserable, or happy and strong."
        "The amount of work is the same. \n-Reigler",
        "You're braver than you believe, and stronger than you seem, and smarter than you think. \n-Stephen Richards",
        "Tough times never last, but tough people do. \n-Schuller"
    ]

    quiz = [
        "The tallest building in the world is located in which city?",
        "Which year was the original Toy Story film released in the US?",
        "Name the current UK Home Secretary",
        "What does BBC stand for?",
        "What nut is used to make marzipan?",
        "What element does 'O' represent in the periodic table?",
        "What is the name of the river that runs through Egypt?",
        "Who played Jack Sparrow in Pirates Of The Caribbean?"
    ]

    answers = [
        "Dubai",
        "1995",
        "Priti Patel",
        "British Broadcasting Corporation",
        "Almonds",
        "Oxygen",
        "Nile River",
        "Johnny Depp"
    ]

    if len(command) == 0:
        return
    elif command == 'help':
        response = 'Thank you for using mangoBot! The current available commands are: !help, !hello, !quote, !quiz'
        await message.channel.send(response)
    elif command == 'hello':
        response = random.choice(greetings)
        await message.channel.send(response)
    elif command == 'quote':
        response = random.choice(quotes)
        await message.channel.send(f"{message.author.mention}\n" + response)
    elif command == 'quiz':
        index = random.randint(0, 2)
        response = quiz[index]
        answer = str(answers[index])
        print(answer)
        await message.channel.send(response)

        def check(m):
            return m.author == message.author

        try:
            msg = (await client.wait_for('message', timeout=15.0, check=check)).content.lower()
        except asyncio.TimeoutError:
            await message.channel.send("Time is up. The correct answer is: {0}".format(answer))
            return
        if msg == answer.lower():
            await message.channel.send("That's right!")
        else:
            await message.channel.send("The correct answer is: {0}".format(answer))
    elif command == "hearye":
        await message.channel.send(file=discord.File('hearye.png'))
    elif command == "clan-info":
        key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc2YWYzMGJmLWFjYzgtNGE0Ny1hZmU2LWIwZjE0NzY2ZWNlYyIsImlhdCI6MTU5MjMxMzY0OSwic3ViIjoiZGV2ZWxvcGVyL2JjNzVkYTRmLTEyMGItOWU3Ny0xMTA0LWM0YmQxMDllMDc5OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.czFtTMv7pqaziRUiivFYyXdvwAvPQNpI7w9tNvrExj0cvzYFl20GHtdLL3LiVKM-ZUFs1wTXeSqfjXgygssT2g"
        base_url = "https://proxy.royaleapi.dev/v1"

        endpoint1 = "/clans/%23L2208GR9/members"
        endpoint2 = "/clans/%23L2208GR9/currentwar"

        request1 = requests.get(base_url + endpoint1, headers={"Authorization": "Bearer %s" % key})

        request2 = requests.get(base_url + endpoint2, headers={"Authorization": "Bearer %s" % key})

        data1 = request1.json()

        data2 = request2.json()

        response1 = ""
        response2 = ""

        if args[1] == "member":
            for item in data1['items']:
                if item['name'] == args[2]:
                    response1 = "Name: {0} \nRank: {1} \nTrophies: {2} \nArena: {3} \nDonations: {4} \n".format(item['name'],
                                                                                                        item['role'],
                                                                                                        item["trophies"],
                                                                                                        item['arena']['name'],
                                                                                                        item["donations"])
                    await message.channel.send(response1)
                    break
            if response1 == "":
                await message.channel.send("Cannot find name.")

        if args[1] == "war":
            if data2['state'] == "notInWar":
                await message.channel.send("We are currently not in war.")
                return
            for item in data2['participants']:
                if item['name'] == args[2]:
                    response2 = "Name:{0} \nCollection Day: {1}/3 \nBattles Played: {2}/{3} \nWins: {4}/{2} \n".format(item['name'],
                                                                                                               item['collectionDayBattlesPlayed'],
                                                                                                               item["battlesPlayed"],
                                                                                                               item['numberOfBattles'],
                                                                                                               item['wins'])
                    await message.channel.send(response2)
                    break
            if response2 == "":
                await message.channel.send("Cannot find name.")


# ===================================================== #

client.run('NzI1Nzg1OTQ4MDgzNzE2MTI2.XvjCHg.2Eixr_ZjK1nvEXlZKH-vMnIpOHY')
