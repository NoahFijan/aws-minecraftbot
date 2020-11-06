import discord
import random
import io
import aiohttp
import json
import subprocess
from discord.ext import commands

def getToken():
    with open('resources/token.txt') as f:
        for line in f:
            token = line.strip('\n')
        return token


token = getToken()
bot = commands.Bot(command_prefix = '.')
channel = discord.utils.get(bot.get_all_channels(), guild__name='test', name='general')


def get_worlds():
    
    worlds = {}

    with open('resources/worlds') as f:
        for line in f:
            worldName,instanceid = line.replace('\n','').split(':')
            worlds[worldName] = instanceid

    return worlds

@bot.event
async def on_ready():
    print('Ready!')

@bot.command()
async def purge(ctx, num = 0):
    msgs = []
    async for msg in ctx.message.channel.history(limit = int(num)):
        msgs.append(msg)
    if ctx.author.id == 144284500162117642 or ctx.author.id == 143833561277923328:
        await ctx.message.channel.delete_messages(msgs)

@bot.command(help='get status of all runing worlds')
async def status(ctx):
    '''
    just checks if the aws instance is running, not if the minecraft 
    server application is running in the container
    
    TODO:
    check if minecraft server application is running rather than if instance is running
    '''

    instances = json.loads(subprocess.check_output('scripts/getinstances.sh', shell=True))
    
    output = []

    worlds = get_worlds() #maybe a dictionary is not the best idea for this?
   
    for instanceid in instances:
        for world in worlds.keys():
            if instanceid == worlds.get(world):
                output.append(world)

    oneworld = True if len(output) == 1 else False

    if len(output):
        await ctx.send(f'World{"" if oneworld else "s"} {", ".join(output)} {"is" if oneworld else "are"} running')
    else:
        await ctx.send('No worlds are currently running')

@bot.command(help='Start specified Minecraft world')
async def start(ctx, server=None):
    
    if server == None:
        await ctx.send('```Usage: .start <name of world>```')

    worlds = get_worlds()

    instances = json.loads(subprocess.check_output('scripts/getinstances.sh', shell=True))

    if worlds.get(server) in instances:
        instanceid = worlds.get(server)

        ip = subprocess.check_output(f'scripts/getinstanceip.sh {instanceid}', shell=True).decode('utf-8').strip('\n')

        await ctx.send(f'{server} should already be online, it can be reached at {ip}:25565')

    else:
        await ctx.send(f'Starting {server}...')
        
        instanceid = worlds.get(server)

        ip = subprocess.check_output(f'scripts/startinstance.sh {instanceid}', shell=True).decode('utf-8').strip('\n')

        await ctx.send(f'{server} can now be reached at {ip}:25565')

@bot.command(help='Stop specified Mincraft world')
async def stop(ctx, server=None):
    '''
    manual command to shut down an aws instance, might make ths exclusive to 
    me/admins just in case
    '''

    if server == None:
        await ctx.send('```Usage: .start <name of world>```')
    
    worlds = get_worlds()

    instances = json.loads(subprocess.check_output('scripts/getinstances.sh', shell=True))

    if worlds.get(server) in instances:
        instanceid = worlds.get(server)

        subprocess.call(f'scripts/stopinstance.sh {instanceid}', shell=True)

        await ctx.send(f'{server} has been shut down')

    else:
        await(f'{server} could not be found. Are you sure it exists and is running?')
        await(f'use: .stats to check the currently running servers')

bot.run(token)



