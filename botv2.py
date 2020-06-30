import os
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='hello', help='mangoBot greets you.')
async def greet(ctx):
    greetings = [
        "Hello, I am mangoBot :)",
        "How are you doing?",
        "I love mango~",
        "Good day!"
    ]
    response = random.choice(greetings)
    await ctx.send(response)

bot.run('NzI1Nzg1OTQ4MDgzNzE2MTI2.XvjCHg.2Eixr_ZjK1nvEXlZKH-vMnIpOHY')