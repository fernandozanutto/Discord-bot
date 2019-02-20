import discord
import asyncio
from time import time

token_file = open('token.txt', 'r')
token = token_file.readline()[:-1]
client = discord.Client(status="Sugooooi")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):

        tmp = await message.channel.send('Yeee, estou funcionando')


@client.event
async def on_member_update(before, after):

    now = time()

    for activity in before.activities:
        if activity.type == discord.ActivityType.playing:

            diferenca = now - activity.timestamps['start']/1000

            #if before.dm_channel is None:
            #    await before.create_dm()

            mensagem = '{} jogou {} por {} segundos'.format(before.mention, activity.name, diferenca)
            #await before.dm_channel.send(mensagem)
            await before.guild.text_channels[0].send(mensagem)


client.run(token)


#keep track of most played game
#keep track of who played most time
