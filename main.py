
import os
from time import sleep

import discord
from discord.ext import commands
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ID_ADMIN = os.getenv('ID_ADMIN')
ID_ADMIN_2 = os.getenv('ID_ADMIN_2')

bot = commands.Bot(command_prefix='$')

language = 'pt-br'
saudacao = ''
voice_channel_conntected = None
channel = None


@bot.event
async def on_voice_state_update(client, before, after):
    try:
        if (str(client.id) == ID_ADMIN):
            sleep(1)
            voice_channel_conntected.play(discord.FFmpegPCMAudio(
                "saudacao-rei.mp3"), after=lambda e: print('done', e))
            await client.guild.system_channel.send('Opa')
        elif (after.channel.name == channel.name):
            sleep(1)
            voice_channel_conntected.play(discord.FFmpegPCMAudio(
                "saudacao.mp3"), after=lambda e: print('done', e))
            await client.guild.system_channel.send('Opa')
    except:
        pass


@bot.command(name="vem-aqui", help="Entrar em um canal de voz")
async def entrar_canal_voz(client):
    global voice_channel_conntected, channel
    author = client.message.author
    channel = author.voice.channel
    voice_channel_conntected = await channel.connect()


@bot.command(name="salva-saudacao", help="Salvar a saudação")
async def salvar_saudacao(client, saudacao_):
    print(client.author.id)
    if (str(client.author.id) == ID_ADMIN or str(client.author.id) == ID_ADMIN_2):
        global saudacao
        saudacao = saudacao_
        myobj = gTTS(text=saudacao, lang=language, slow=False)
        myobj.save('saudacao.mp3')
        await client.send("Saudação salva!")
    else:
        await client.send("Ei {0} tu é doido é ? Tá achando que é o rei ".
                          format(client.author.name) + "Rick slk")


@bot.command(name="saudacao", help="Qual a saudação salva")
async def get_saudacao(client):
    await client.send("A saudação salva é {0}".format(saudacao))


@bot.command(name="sai-daqui", help="Sair do canal de voz")
async def leave(client):
    await client.voice_client.disconnect()

bot.run(TOKEN)
