import os
import discord
import GameElements
from dotenv import load_dotenv
from discord.ext import commands

PLAYER_ONE = "Player 1"
PLAYER_TWO = "Player 2"
AWAITING = "Awaiting player"


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

        def check(reaction, user):
            return (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣') and not user.bot

        async def login():
            p1assigned, p2assigned = False, False
            p1, p2 = None, None
            while not p1assigned or not p2assigned:
                reaction, user = await bot.wait_for("reaction_add", check=check)
                if str(reaction.emoji) == '1️⃣':
                    if not p1assigned:
                        p1assigned = True
                        p1 = user
                        embedVar.set_field_at(index=0, name=PLAYER_ONE, value=p1.name)
                        await assignmentMessage.edit(embed=embedVar)
                        await reaction.remove(user)
                    else:
                        p1assigned = False
                        p1 = None
                        embedVar.set_field_at(index=0, name=PLAYER_ONE, value=AWAITING)
                        await assignmentMessage.edit(embed=embedVar)
                        await reaction.remove(user)
                elif str(reaction.emoji == '2️⃣'):
                    if not p2assigned:
                        p2assigned = True
                        p2 = user
                        embedVar.set_field_at(index=1, name=PLAYER_TWO, value=p2.name)
                        await assignmentMessage.edit(embed=embedVar)
                        await reaction.remove(user)
                    else:
                        p2assigned = False
                        p2 = None
                        embedVar.set_field_at(index=1, name=PLAYER_TWO, value=AWAITING)
                        await assignmentMessage.edit(embed=embedVar)
                        await reaction.remove(user)
            embedVar.description = "Players locked in!"
            await assignmentMessage.edit(embed=embedVar)
            await assignmentMessage.clear_reactions()
            return p1, p2

        game = GameElements.GameManagerDUI(col, row)
        embedVar = discord.Embed(title="Players", description="Who will be player 1 and player 2?")
        embedVar.add_field(name=PLAYER_ONE, value=AWAITING)
        embedVar.add_field(name=PLAYER_TWO, value=AWAITING)
        assignmentMessage = await ctx.channel.send(embed=embedVar)
        await assignmentMessage.add_reaction('1️⃣')
        await assignmentMessage.add_reaction('2️⃣')
        player1, player2 = await login()
        game.login(player1.name, player2.name)


    bot.run(TOKEN)
