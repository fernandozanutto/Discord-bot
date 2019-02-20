import discord
import asyncio

token_file = open('token.txt', 'r')
token = token_file.readline()[:-1]
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await message.channel.send('Calculating messages...')
        async for log in message.channel.history():
            if log.author == message.author:
                counter += 1
                
        await tmp.edit(content = "You have {} messages.".format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await message.channel.send('Done sleeping')

client.run(token)
