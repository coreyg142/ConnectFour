import os
import discord
import GameElements
from GameElements import Move
from GameElements import Piece
from dotenv import load_dotenv
from discord.ext import commands

PLAYER_ONE = "Player 1 🔴"
PLAYER_TWO = "Player 2 🟡"
AWAITING = "Awaiting player"
TURN_PREFIX = "drop "


def run(row, col):
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='$')

    @bot.event
    async def on_ready():
        print("{} has connected to Discord!".format(bot.user.name))

    @bot.command()
    @commands.is_owner()
    async def shutdown(ctx):
        await ctx.channel.send("Bye bye")
        await bot.logout()
        print("Shutdown complete")

    @bot.command(name='newgame')
    async def connectFour(ctx):

        def checkLogin(reaction, user):
            return (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣') and not user.bot and \
                   reaction.message == assignmentMessage

        def checkInp(user):
            def innerCheckInp(msg):
                return msg.author == user and msg.content.startswith(TURN_PREFIX)

            return innerCheckInp

        async def login():
            p1assigned, p2assigned = False, False
            p1, p2 = None, None
            while not p1assigned or not p2assigned:
                reaction, user = await bot.wait_for("reaction_add", check=checkLogin)
                if str(reaction.emoji) == '1️⃣':
                    if not p1assigned:
                        p1assigned = True
                        p1 = user
                        loginEmbed.set_field_at(index=0, name=PLAYER_ONE, value=p1.name)
                        await assignmentMessage.edit(embed=loginEmbed)
                        await reaction.remove(user)
                    elif p1assigned and user == p1:
                        p1assigned = False
                        p1 = None
                        loginEmbed.set_field_at(index=0, name=PLAYER_ONE, value=AWAITING)
                        await assignmentMessage.edit(embed=loginEmbed)
                        await reaction.remove(user)
                elif str(reaction.emoji == '2️⃣'):
                    if not p2assigned:
                        p2assigned = True
                        p2 = user
                        loginEmbed.set_field_at(index=1, name=PLAYER_TWO, value=p2.name)
                        await assignmentMessage.edit(embed=loginEmbed)
                        await reaction.remove(user)
                    elif p2assigned and user == p2:
                        p2assigned = False
                        p2 = None
                        loginEmbed.set_field_at(index=1, name=PLAYER_TWO, value=AWAITING)
                        await assignmentMessage.edit(embed=loginEmbed)
                        await reaction.remove(user)
            loginEmbed.description = "Players locked in!"
            await assignmentMessage.edit(embed=loginEmbed)
            await assignmentMessage.clear_reactions()
            return p1, p2

        def buildBoardEmbed(curUser, playerStr):
            boardEmbed = discord.Embed(title="Game Board", description="Current turn: \n{}".format(playerStr))
            boardEmbed.add_field(name="Board", value=game.getBoard())
            boardEmbed.add_field(name="Input", value="{}, which column do you wish to drop in?\n"
                                                     "Say \"{} [col]\"".format(curUser, TURN_PREFIX), inline=False)
            return boardEmbed

        async def buildWonEmbed(winner):
            if winner is Piece.red:
                boardEmbed.description = "GAME OVER!"
                boardEmbed.set_field_at(index=0, name="Board", value=game.getBoard())
                boardEmbed.set_field_at(index=1, name="WINNER: ", value="{} has won the game!".format(player1.name),
                                        inline=False)
                await boardMessage.edit(embed=boardEmbed)
            else:
                boardEmbed.description = "GAME OVER!"
                boardEmbed.set_field_at(index=0, name="Board", value=game.getBoard())
                boardEmbed.set_field_at(index=1, name="WINNER: ", value="{} has won the game!".format(player2.name),
                                        inline=False)
                await boardMessage.edit(embed=boardEmbed)

        async def mainloop():
            board = game.getBoard()
            isOver = False
            winner = Piece.empty

            while not isOver:
                await handleInpMove(player1, PLAYER_ONE, game.getPlayer(1), board)
                isOver, winner = board.checkIfWinner()
                if isOver: break
                await handleInpMove(player2, PLAYER_TWO, game.getPlayer(2), board)
                isOver, winner = board.checkIfWinner()

            print("Game over!")
            await buildWonEmbed(winner)

        async def handleInpMove(user, playerStr, player, board):
            boardEmbed = buildBoardEmbed(user.name, playerStr)
            await boardMessage.edit(embed=boardEmbed)
            inp = await playerInput(user, board)
            board.makeMove(player.getTeam(), inp)

        async def playerInput(player, board):
            dim = board.getMaxCol()
            while True:
                print("awaiting input")
                inpMsg = await bot.wait_for('message', check=checkInp(player))
                await inpMsg.delete()
                try:
                    inp = int(inpMsg.content.split(" ")[1]) - 1
                    isValid = board.isValidMove(inp)
                    if isValid is Move.VALID:
                        return inp
                    elif isValid is Move.OUT_OF_BOUNDS:
                        boardEmbed.set_field_at(index=0, name="Board", value=game.getBoard())
                        boardEmbed.set_field_at(index=1, name="Input Error, try again", value=str(isValid) + str(dim),
                                                inline=False)
                        await boardMessage.edit(embed=boardEmbed)
                    elif isValid is Move.COL_FULL:
                        boardEmbed.set_field_at(index=0, name="Board", value=game.getBoard())
                        boardEmbed.set_field_at(index=1, name="Input Error, try again", value=str(isValid),
                                                inline=False)
                        await boardMessage.edit(embed=boardEmbed)
                except ValueError:
                    boardEmbed.set_field_at(index=0, name="Board", value=game.getBoard())
                    boardEmbed.set_field_at(index=1, name="Input Error, try again", value="Please input a number",
                                            inline=False)
                    await boardMessage.edit(embed=boardEmbed)

        game = GameElements.GameManagerDUI(col, row)
        loginEmbed = discord.Embed(title="Players", description="Who will be user 1 and user 2?")
        loginEmbed.add_field(name=PLAYER_ONE, value=AWAITING)
        loginEmbed.add_field(name=PLAYER_TWO, value=AWAITING)
        assignmentMessage = await ctx.channel.send(embed=loginEmbed)
        await assignmentMessage.add_reaction('1️⃣')
        await assignmentMessage.add_reaction('2️⃣')
        player1, player2 = await login()
        game.login(player1.name, player2.name)

        boardEmbed = buildBoardEmbed(player1, PLAYER_ONE)
        boardMessage = await ctx.channel.send(embed=boardEmbed)
        await mainloop()

    bot.run(TOKEN)
