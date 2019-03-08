import discord
from discord.ext import commands
from time import time
from datetime import datetime
from calendar import monthrange
import youtube
import db

db.create_table()

token_file = open('token.txt', 'r')

TOKEN = token_file.readline()[:-1]
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX, activity=discord.Game(name="{}help".format(PREFIX)))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def formatar_data_limite(tempo: str):
    data_limite = None
    hoje = datetime.fromtimestamp(time())

    if tempo == "mes":
        data_inicio = hoje.replace(day = 1, hour = 0, minute = 0, second = 0)
        data_fim = hoje.replace(day = monthrange(hoje.year, hoje.month)[1], hour = 23, minute = 59, second = 59)

        data_limite = (data_inicio.strftime('%Y-%m-%d %H:%M:%S'), data_fim.strftime('%Y-%m-%d %H:%M:%S'))

    elif tempo == "dia":
        data_inicio = hoje.replace(hour = 0, minute = 0, second = 0)
        data_fim = hoje.replace(hour = 23, minute = 59, second = 59)

        data_limite = (data_inicio.strftime('%Y-%m-%d %H:%M:%S'), data_fim.strftime('%Y-%m-%d %H:%M:%S'))

    return data_limite


@bot.group(pass_context=True, invoke_without_command=True)
async def leaderboard(ctx, tempo: str = ""):
    """Membros por ordem de quem mais passou tempo jogando"""

    data_limite = formatar_data_limite(tempo)

    membros = [x for x in ctx.guild.members if not x.bot]

    resultado = db.leaderboard_usuarios([member.id for member in membros], data_limite)

    dic_membros = {member.id: member for member in membros}

    mensagem = ""

    for registro in resultado:
        mensagem += "\n{0.mention} jogou por {1:.2f} minutos".format(dic_membros.pop(registro[0]), registro[1])

    for k,v in dic_membros.items():
        mensagem += "\n{0.mention} jogou por 0 minutos".format(v)

    await ctx.send(mensagem)

@leaderboard.command(pass_context=True)
async def jogos(ctx, tempo: str = ""):
    """Jogos por ordem de tempo que foi jogado"""

    data_limite = formatar_data_limite(tempo)

    resultado = db.leaderboard_jogos(data_limite)

    mensagem = ""
    for registro in resultado:
        mensagem += "\n{0[0]} jogado por {0[1]:.2f} minutos".format(registro)

    await ctx.send(mensagem)

@bot.event
async def on_message(message):

    if not message.author.bot:
        try:
            pass
            #print("resultado do eval: \n" + str(eval(message.content)))
            #await message.channel.send("resultado do eval: \n" + str(eval(message.content)))
        except Exception as e:
            pass
            #print("erro no eval: " + str(message.content) + " " + str(e))

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
                    data2 = data_inicio.replace(hour = 23, minute = 59, second = 59)
                    data4 = data_fim.replace(hour = 0, minute = 0, second = 0)

                    db.insert(before.id, activity.application_id, data_inicio.strftime('%Y-%m-%d %H:%M:%S'), data2.strftime('%Y-%m-%d %H:%M:%S'), activity.name)
                    db.insert(before.id, activity.application_id, data4.strftime('%Y-%m-%d %H:%M:%S'), data_fim.strftime('%Y-%m-%d %H:%M:%S'), activity.name)

                else:
                    db.insert(before.id, activity.application_id, data_inicio.strftime('%Y-%m-%d %H:%M:%S'), data_fim.strftime('%Y-%m-%d %H:%M:%S'), activity.name)


                mensagem = '{} jogou {} por {:.2f} minutos'.format(before.mention, activity.name, diferenca/60)
                await before.guild.text_channels[0].send(mensagem)

                #if before.dm_channel is None:
                #    await before.create_dm()
                #await before.dm_channel.send(mensagem)

            except Exception as e:
                    print("erro em atividade: " + activity.name)
                    print(e)

youtube.setup(bot)
bot.run(TOKEN)
