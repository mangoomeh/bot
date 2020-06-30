import discord
import random
import asyncio

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
# ===================================================== #

client.run('NzI1Nzg1OTQ4MDgzNzE2MTI2.XvjCHg.2Eixr_ZjK1nvEXlZKH-vMnIpOHY')