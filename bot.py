import discord
from discord.ext import commands
from time import time
from datetime import datetime
from calendar import monthrange
import db

db.create_table()

token_file = open('token.txt', 'r')
token = token_file.readline()[:-1]

bot = commands.Bot(command_prefix="!", activity=discord.Game(name="Testing"))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def teste(ctx):
    await ctx.send("Yee, estou funcionando")

@bot.group(pass_context=True, invoke_without_command=True)
async def leaderboard(ctx, tempo: str = ""):
    """Membros por ordem de quem mais passou tempo jogando"""

    membros = [x for x in ctx.guild.members if not x.bot]

    resultado = db.leaderboard_usuarios([member.id for member in membros])

    tempos = {member.id: 0 for member in membros}
    dic_membros = {member.id: member for member in membros}

    for registro in resultado:
        id_usuario, jogo, inicio, fim = registro

        datetime_inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M:%S')
        datetime_fim = datetime.strptime(fim, '%Y-%m-%d %H:%M:%S')

        diferenca = (datetime_fim - datetime_inicio).seconds

        tempos[id_usuario] += diferenca

    mensagem = ""

    for id_usuario, tempo in sorted(tempos.items(), key=lambda x: x[1], reverse=True):
        mensagem += "\n{0.mention} jogou por {1:.2f} minutos".format(dic_membros[id_usuario], tempo/60)

    await ctx.send(mensagem)

@leaderboard.command(pass_context=True)
async def jogos(ctx):
    """Jogos por ordem de tempo que foi jogado"""
    """
    hoje = datetime.fromtimestamp(time())
    data_inicio = ""
    data_fim = ""

    if tempo == "mes":

        data_inicio = hoje
        data_inicio.day = 1
        data_inicio.hour = 0
        data_inicio.minute = 0
        data_inicio.second = 0

        data_fim = hoje
        data_fim.day = monthrange(hoje.year, hoje.month)[0]
        data_fim.hour = 23
        data_fim.minute = 59
        data_fim.second = 59

    elif tempo == "dia":
        data_inicio = hoje
        data_inicio.hour = 0
        data_inicio.minute = 0
        data_inicio.second = 0

        data_fim = hoje
        data_fim.hour = 23
        data_fim.minute = 59
        data_fim.second = 59

    data_limite = (data_inicio, data_fim)
    """

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
