
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
greeting = 'O gado chegou'
greeting_king = 'O rei chegou pessoal. Abram espaço!'
voice_channel_conntected = None
channel = None


def save_audio(type_greeting: str):
    if type_greeting == 'greeting':
        myobj = gTTS(text=greeting, lang=language, slow=False)
        myobj.save('greeting.mp3')
    elif type_greeting == 'greeting_king':
        myobj = gTTS(text=greeting_king, lang=language, slow=False)
        myobj.save('greeting_king.mp3')


save_audio('greeting')
save_audio('greeting_king')


@bot.event
async def on_voice_state_update(client, before, after):
    try:
        print(client.id)
        roles_in_user = list(
            filter(lambda role: role.name == 'GADO', client.roles))
        if str(client.id) in [ID_ADMIN, ID_ADMIN_2]:
            sleep(3)
            voice_channel_conntected.play(discord.FFmpegPCMAudio(
                executable="ffmpeg.exe",
                source="greeting_king.mp3"))
            await client.guild.system_channel.send('O Rei chegou :)')
        elif roles_in_user:
            sleep(3)
            voice_channel_conntected.play(discord.FFmpegPCMAudio(
                executable="ffmpeg.exe",
                source="greeting.mp3"))
            await client.guild.system_channel.send('Pegamos um gado :)')

    except Exception as ex:
        msg = 'O meu desenvolvedor fez alguma merda! Ou foi você ? :´)'
        await client.guild.system_channel.send(msg)
        print("Ocorreu alguma coisinha: {}".format(ex))


@bot.command(name="vem-aqui", help="Entrar em um canal de voz")
async def entrar_canal_voz(client):
    global voice_channel_conntected, channel
    author = client.message.author
    channel = author.voice.channel
    voice_channel_conntected = await channel.connect()


@bot.command(name="salva-saudacao-rei", help="Salvar a saudação dos reis")
async def salvar_saudacao_rei(client, greeting_king_):
    print(client.author.id)
    if str(client.author.id) in [ID_ADMIN, ID_ADMIN_2]:
        global greeting_king
        greeting_king = greeting_king_
        myobj = gTTS(text=greeting_king, lang=language, slow=False)
        myobj.save('greeting_king.mp3')
        await client.send("Saudação salva!")
    else:
        await client.send("Ei {0} tu é doido é ? Tá achando que é o Rei Rich".
                          format(client.author.name))


@bot.command(name="salva-saudacao", help="Salvar a saudação")
async def salvar_saudacao(client, greeting_):
    print(client.author.id)
    if str(client.author.id) in [ID_ADMIN, ID_ADMIN_2]:
        global greeting
        greeting = greeting_
        myobj = gTTS(text=greeting, lang=language, slow=False)
        myobj.save('greeting.mp3')
        await client.send("Saudação salva!")
    else:
        await client.send("Ei {0} tu é doido é ? Tá achando que é o Rei Rich".
                          format(client.author.name))


@bot.command(name="saudacao", help="Qual a saudação salva")
async def get_saudacao(client):
    await client.send("A saudação salva é {0}".format(greeting))


@bot.command(name="sai-daqui", help="Sair do canal de voz")
async def leave(client):
    await client.voice_client.disconnect()

bot.run(TOKEN)
