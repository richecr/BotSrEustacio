import os
import asyncio
from time import sleep

import discord
from discord.ext import commands
from dotenv import load_dotenv
from duck_orm.sql.condition import Condition
from gtts import gTTS

from database.db import database
from models.User import User
from models.Greeting import Greeting

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ID_ADMIN = os.getenv("ID_ADMIN")
ID_ADMIN_2 = os.getenv("ID_ADMIN_2")
ID_ADMIN_3 = os.getenv("ID_ADMIN_3")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

language = "pt-br"
greeting_default = "Chegou o disco voador!"
greeting_cattle = "O gado chegou"
greeting_finin = "é o finas"
greeting_king = "O rei chegou pessoal. Abram espaço!"
voice_channel_conntected = None
channel = None


def record_audio(greeting: str):
    """
    Method that perform record the audio with greeting of the client.

    PARAMS
        - greeting: `str` - The Greeting
    """
    myobj = gTTS(text=greeting, lang=language, slow=False)
    myobj.save("greeting.mp3")


@bot.event
async def on_voice_state_update(client, before, after):
    try:
        if client in after.channel.members:
            roles_in_user = list(filter(lambda role: role.name == "GADO", client.roles))
            greetings = await Greeting.find_all(
                conditions=[Condition("id_user", "=", str(client.id))]
            )
            if roles_in_user:
                record_audio(greeting_cattle)
            elif greetings:
                # TODO: User can have multiple greetings
                #           - Draw the greeting ?
                greeting = greetings[0].greeting
                record_audio(greeting)
            else:
                record_audio(greeting_default)

            sleep(1.5)
            voice_channel_conntected.play(
                source=discord.FFmpegPCMAudio(
                    source="greeting.mp3",
                    executable="ffmpeg.exe",
                )
            )
    except Exception as ex:
        print(f"Ocorreu alguma coisinha: {ex}")


@bot.command(name="vem-aqui")
async def join(ctx, *, channel: discord.VoiceChannel):
    global voice_channel_conntected
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    voice_channel_conntected = await channel.connect()


@bot.command(name="salva-saudacao", help="Salvar a saudação dos reis")
async def save_greeting(client, greeting_user: str):
    try:
        if len(greeting_user) < 2:
            await client.send("A saudação deve ter mais de 2 letras! :(")
        else:
            author = client.author
            await User.save(User(id=str(author.id), name=author.name))
            await Greeting.save(
                Greeting(greeting=greeting_user, id_user=str(author.id))
            )
            msg = f"A saudação {greeting_user} foi salva, Sr(a). {author.name}"
            await client.send(msg)
    except Exception:
        msg = "Aconteceu alguma coisa inesperada hein :(\nChama o SUPORTE"
        await client.send(msg)


@bot.command(name="saudacao", help="Qual a saudação salva")
async def get_greeting(client):
    try:
        greetings = await Greeting.find_all(
            conditions=[Condition("id_user", "=", str(client.author.id))]
        )
        greeting = greetings[0].greeting
        await client.send(
            "A sua Sr. {} saudação salva é {}".format(client.author.name, greeting)
        )
    except Exception:
        msg = "Sem saudação encontrada. Tu tem quem adicionar antes Mula e eu não vou dizer qual o comando!"
        await client.send(msg)


@bot.command(name="sai-daqui", help="Sair do canal de voz")
async def leave(client):
    await client.voice_client.disconnect()


async def main():
    await database.connect()
    await User.create()
    await Greeting.create()


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())

bot.run(TOKEN)
