import discord
from discord.ext import commands
from time import time
from datetime import datetime
import db

db.create_table()

token_file = open('token.txt', 'r')
token = token_file.readline()[:-1]

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name="Testando"))


@bot.command()
async def teste(ctx):
    await ctx.send("Yee, estou funcionando")

@bot.command()
async def leaderboard(ctx):
    #quem mais jogou no total

    resultado = db.leaderboard([member.id for member in ctx.guild.members])

    tempos = {member.id: 0 for member in ctx.guild.members}

    for registro in resultado:
        id_usuario, jogo, inicio, fim = registro

        datetime_inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M:%S')
        datetime_fim = datetime.strptime(fim, '%Y-%m-%d %H:%M:%S')

        diferenca = (datetime_fim - datetime_inicio).seconds

        tempos[id_usuario] += diferenca

    mensagem = ""

    for member in ctx.guild.members:
        if not member.bot:
            mensagem += "\n{0.mention} jogou por {1} minutos".format(member, tempos[member.id]/60)

    await ctx.send(mensagem)

@bot.event
async def on_message(message):
    if not message.author.bot:
        try:
            print("resultado do eval: \n" + str(eval(message.content)))
            await message.channel.send("resultado do eval: \n" + str(eval(message.content)))
        except Exception as e:
            print("erro no eval: " + str(message.content) + " " + str(e))

    await bot.process_commands(message)


@bot.event
async def on_member_update(before, after):

    if before.bot:
        return

    end = int(time())

    for activity in before.activities:
        if activity.type == discord.ActivityType.playing:
            try:
                start = activity.timestamps['start'] // 1000
                diferenca = end - start

                data_inicio = datetime.fromtimestamp(start)
                data_fim = datetime.fromtimestamp(end)

                if data_inicio.day != data_fim.day:
                    data2 = data_inicio
                    data2.hour = 23
                    data2.minute = 59
                    data2.second = 59

                    data4 = data_fim
                    data4.hour = 0
                    data4.minute = 0
                    data4.second = 0

                    db.insert(before.id, activity.application_id, data_inicio.strftime('%Y-%m-%d %H:%M:%S'), data2.strftime('%Y-%m-%d %H:%M:%S'), activity.name)
                    db.insert(before.id, activity.application_id, data4.strftime('%Y-%m-%d %H:%M:%S'), data_fim.strftime('%Y-%m-%d %H:%M:%S'), activity.name)

                else:
                    db.insert(before.id, activity.application_id, data_inicio.strftime('%Y-%m-%d %H:%M:%S'), data_fim.strftime('%Y-%m-%d %H:%M:%S'), activity.name)

                #if before.dm_channel is None:
                #    await before.create_dm()

                mensagem = '{} jogou {} por {:.2f} minutos'.format(before.mention, activity.name, diferenca/60)
                #await before.dm_channel.send(mensagem)
                await before.guild.text_channels[0].send(mensagem)

            except:
                    print("erro em atividade: " + activity.name)


bot.run(token)

#keep track of most played game
#keep track of who played most time
