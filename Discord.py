import os
import discord
import GameElements
from dotenv import load_dotenv
from discord.ext import commands

PLAYER_ONE = "Player 1"
PLAYER_TWO = "Player 2"

def run(row, col):
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='$')

    @bot.event
    async def on_ready():
        print("{} has connected to Discord!".format(bot.user.name))


    @bot.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(ctx):
        await ctx.channel.send("Bye bye")
        await bot.logout()
        print("Shutdown complete")

    @bot.command()
    async def newgame(ctx):
        game = GameElements.GameManagerDUI(col, row)
        await ctx.channel.send("Who will be player 1? Say \"me!\"")
        player1 = await login(ctx, bot, PLAYER_ONE)
        await ctx.channel.send("Who will be player 2? Say \"me!\"")
        player2 = await login(ctx, bot, PLAYER_TWO)

        print("{}".format(player1.bot))

        game.login(player1.name, player2.name)

    bot.run(TOKEN)


async def login(ctx, bot, player):
    msg = await bot.wait_for("message", check=check)
    await ctx.channel.send("{} is {}!".format(msg.author, player))
    return msg.author


def check(msg):
    return msg.content == "me!" and not msg.author.bot
