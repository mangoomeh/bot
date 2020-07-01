import discord
import os
import asyncio
import random
import requests

client = discord.Client()

# ================================================ #


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
        "Tough times never last, but tough people do. \n-Schuller",
        "Be yourself; everyone else is already taken. \n-Wilde",
        "Strive not to be a success, but rather to be of value. \n-Albert Einstein",
        "You miss 100% of the shots you don't take. \n-Wayne Gretzky",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "Your time is limited, so don't waste it living someone else's live. \n-Steve Jobs",
        "You can never cross the ocean until you have the courage to lose sign of the shore. \n-Columbus"
        ]

    quiz = [
        "The tallest building in the world is located in which city?", #1
        "Which year was the original Toy Story film released in the US?", #2
        "Name the current UK Home Secretary",#3
        "What does BBC stand for?",#4
        "What nut is used to make marzipan?",#5
        "What element does 'O' represent in the periodic table?",#6
        "What is the name of the river that runs through Egypt?",#7
        "Who played Jack Sparrow in Pirates Of The Caribbean?",#8
        "What year was the very first model of the iPhone released?",#9
        "What is meteorology the study of?",#10
        "Which planet is the hottest in the solar system?",#11
        "What part of the atom has no electric charge?",#12
        "What is the chemical symbol for potassium?",#13
        "Which planet has the most gravity?",#14
        "Which animal can be seen on the Porsche logo?",#15
        "How many parts (screws and bolts included) does the average car have?",#16
        "Which country produces the most coffee in the world?",#17
        "Which country invented tea?",#18
        "Which brand of alcohol is Russia notoriously known for?",#19
        "Which European nation was said to invent hot dogs?",#20
        "Which country is responsible for giving us pizza and pasta?",#21
        "What percentage of our bodies is made up of water?",#22
        "What is the largest organ?",#23
        "What kind of cells are found in the brain?",#24
        "Which continent is the largest?",#25
        "Which desert is the largest in the world?",#26
        "Which two countries share the longest (or largest) international border?",#27
        "What is the smallest country in the world?",#28
        "What genre of music did Taylor Swift start in?",#29
        "How many Lord of the Rings films are there?",#30
        "Who played Jack Dawson (main male lead) in Titanic? (full name)",#31
        "In what year was the first episode of South Park aired?",#32
        "How many hearts does an octopus have?",#33
        "How many eyes does a bee have?",#34
        "What is the fastest land animal?",#35
        "24 x (3 + 4) + 88 = ?",#36
        "37 x (2 + 3) + 59 = ?",#37
        "17 x (5 + 4) + 44 = ?",#38
        "67 x (2 + 1) + 93 = ?",#39
        "87 x 7 + 95 = ?",#40
        "5! = ?",#41
        "1 + 2 + 3.. + 10 = ?",#42
        "What is my name?",#43
        "T or F? Pi can be written correctly as a fraction.",#44
        "Which is bigger? Googol or billion?",#45
        "T or F? All sides are equal in an Isoceles triangle.",#46
        "Which mathematical symbol was determined by Whiz Ferdinand Von Lindemann 1882?",#47
        "An angle more than 90 degrees but less than 180 degrees is called?",#48
        "Number system with the base of 2 is called?",#49
        "Polygon with eight sides called?",#50
        "An improper fraction is always greater than what number?",#51
        "The ancient Babylonians had their number system based on?",#52
        "Which is the most ancient? Fibonacci, Kaprekar, Mersenne or Figurate?",#53
        "How many prime numbers are there between 1 to 10?",#54
        "What comes next in the Fibonacci sequence: 0,1,1,2,3,5,8,13 __?",#55
        "Number system with the base of 12 is called?",#56
        "Which year was Minecraft released?",#57
        "What does Mario jump on after completing a level?",#58
        "What does NES stand for?",#59
        "Which planet size is approximately the same as Minecraft?",#60
        "Name the character abused by Mario",#61
        "In the game Overcooked, which kingdom is in danger?",#62
        "T or F? Epic is better than Rare.",#63
        "Name the arena where elite barbarians card is unlocked.",#64
        "How many trophies to reach PEKKA Playhouse?",#65
        "T or F? Each player has 3 princess towers.",#66
        "Highest damage spell in clash royale?",#67
        "What is the name of the first arena in clash royale?",#68
        "When was Clash Royale originally released?",#69
        "How many hours does Giant Chest take to open?",#70
        "How many hours does Magical Chest take to open?"#71
    ]

    answers = [
        "Dubai",#1
        "1995",#2
        "Priti Patel",#3
        "British Broadcasting Corporation",#4
        "Almonds",#5
        "Oxygen",#6
        "Nile River",#7
        "Johnny Depp",#8
        "2007",#9
        "The Weather",#10
        "Venus",#11
        "Neutron",#12
        "K",#13
        "Jupiter",#14
        "Horse",#15
        "30000",#16
        "Brazil",#17
        "China",#18
        "Vodka",#19
        "Germany",#20
        "Italy",#21
        "60-65%",#22
        "Skin",#23
        "Neurons",#24
        "Asia",#25
        "Sahara",#26
        "Canada and USA",#27
        "Vatican City",#28
        "Country",#29
        "3",#30
        "Leonardo DiCaprio",#31
        "1997",#32
        "3",#33
        "5",#34
        "Cheetah",#35
        "256",#36
        "244",#37
        "197",#38
        "294",#39
        "704",#40
        "120",#41
        "55",#42
        "mangoBot",#43
        "F",#44
        "Googol",
        "F",#45
        "Pi",#46
        "Obtuse",#47
        "Binary",#48
        "Octagon",#49
        "1",#50
        "60",#51
        "Figurate",#52
        "4",#53
        "21",#54
        "Duodecimal",#55
        "2009",#56
        "Flag pole",#57
        "Nintendo Entertainment System",#58
        "Neptune",#59
        "Donkey Kong",#60
        "Onion Kingdom",#61
        "F",#62
        "Hog Mountain",#63
        "1000",#64
        "F",#65
        "Rocket",#66
        "Goblin Stadium",#67
        "4 January 2016",#68
        "12",#69
        "12"#70
    ]

    if len(command) == 0:
        return
    elif command == 'help':
        response = "Thank you for using mangoBot! The current available commands are: !help, !hello, !quote, !quiz, !clan-info (war/member).'name of player'."
        await message.channel.send(response)
    elif command == 'hello':
        response = random.choice(greetings)
        await message.channel.send(response)
    elif command == 'quote':
        response = random.choice(quotes)
        await message.channel.send(f"{message.author.mention}\n" + response)
    elif command == 'quiz':
        index = random.randint(0, len(quiz) - 1)
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
            await message.channel.send(message.author.mention + "That's right!")
        else:
            await message.channel.send(message.author.mention + "The correct answer is: {0}".format(answer))
    elif command == "clan-info":
        args2 = message.content.split('.')
        key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc2YWYzMGJmLWFjYzgtNGE0Ny1hZmU2LWIwZjE0NzY2ZWNlYyIsImlhdCI6MTU5MjMxMzY0OSwic3ViIjoiZGV2ZWxvcGVyL2JjNzVkYTRmLTEyMGItOWU3Ny0xMTA0LWM0YmQxMDllMDc5OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.czFtTMv7pqaziRUiivFYyXdvwAvPQNpI7w9tNvrExj0cvzYFl20GHtdLL3LiVKM-ZUFs1wTXeSqfjXgygssT2g"
        base_url = "https://proxy.royaleapi.dev/v1"

        endpoint1 = "/clans/%23L2208GR9/members"
        endpoint2 = "/clans/%23L2208GR9/currentwar"

        request1 = requests.get(base_url + endpoint1, headers={"Authorization": "Bearer %s" % key})

        request2 = requests.get(base_url + endpoint2, headers={"Authorization": "Bearer %s" % key})

        data1 = request1.json()

        data2 = request2.json()

        response = ""
        response1 = ""
        response2 = ""

        if args[1] == "membername":
            for item in data1['items']:
                response = response + item['name'] + "\n"

            await message.channel.send(response)

        if args2[0] == "!clan-info member":
            for item in data1['items']:
                if item['name'] == args2[1]:
                    response1 = "Name: {0} \nRank: {1} \nTrophies: {2} \nArena: {3} \nDonations: {4} \n".format(item['name'],
                                                                                                        item['role'],
                                                                                                        item["trophies"],
                                                                                                        item['arena']['name'],
                                                                                                        item["donations"])
                    await message.channel.send(response1)
                    break
            if response1 == "":
                await message.channel.send("Cannot find name.")

        if args2[0] == "!clan-info war":
            for item in data2['participants']:
                if item['name'] == args2[1]:
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

client.run(os.environ['token'])
