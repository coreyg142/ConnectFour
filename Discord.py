import os
import discord
import GameElements
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# client = discord.Client()
bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print("{} has connected to Discord!".format(bot.user.name))


# @client.event
# async def on_ready():
#     print(f'{client.user.name} has connected to Discord!')
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content == '!test':
#         embedVar = discord.Embed(title="Title", description="Desc.", color=0x00ff00)
#         embedVar.add_field(name="Field1", value="hi")
#         await message.channel.send(embed=embedVar)
#
#     if message.content == '!board':
#         board = GameElements.Board(6, 7)
#         embedVar = discord.Embed(title="Connect Four Board")
#         embedVar.add_field(name="Board", value=str(board))
#         messageVar = await message.channel.send(embed=embedVar)
#
#         await message.channel.send(str(board))
@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.channel.send("Bye bye")
    await bot.logout()
    print("Shutdown complete")


bot.run(TOKEN)
