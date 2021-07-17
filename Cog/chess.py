# Imports

import asyncio

import chess
import chess.svg
import discord
from discord.ext import commands
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image
message_on_error = True


class Chess(commands.Cog, name="Chess"):
    """Chess commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start")
    async def start(self, ctx, *, user: discord.User):
        """Start a chess game with someone!"""
        await chess_loop(ctx.author, user, ctx, self.bot)  # Load the loop


def setup(bot):
    bot.add_cog(Chess(bot))  # Normal setup stuff


async def chess_loop(user1, user2, ctx, bot):
    # Chess loop
    embed = discord.Embed(title=f"Game started!",
                          description=f"Check your dms. {user1.mention} is whites and {user2.mention} is blacks.",
                          color=discord.Color.green())
    await ctx.send(embed=embed)
    # Initiate the board
    board = chess.Board()
    # Save the board as an svg
    img = chess.svg.board(board=board)
    outputfile = open('chess_board.svg', "w")
    outputfile.write(img)
    outputfile.close()
    # Convert svg to png
    drawing = svg2rlg("chess_board.svg")
    renderPM.drawToFile(drawing, "chess_board.png", fmt="PNG")
    img = Image.open('chess_board.png')
    img.save('chess_board.png')
    # Send the chess board
    await ctx.send(file=discord.File(fp="chess_board.png"))
    game_over = False
    while game_over is not True:
        # Loop until game is over or canceled. Yes this can be optimized but this was around the time he didnt pay
        cancel = await board_move(user1, board, ctx, bot)
        # Check if game is over
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            # Check if a user canceled
            return
        if game_over:
            # Check if game is over
            embed = discord.Embed(title=f"Game over!",
                                  description=f"{user1.mention} won the game! GG",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            return

        # Basically a repeat of above!
        cancel = await board_move(user2, board, ctx, bot)
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            return
        if game_over:
            embed = discord.Embed(title=f"Game over!",
                                  description=f"{user2.mention} won the game! GG",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            return


async def board_move(player, board, ctx, bot):
    # Move loops
    turn_loop = True
    while turn_loop:
        # Make it a loop so if they make a mistake they can have more attempts
        # could be removed with the check in wait_for message, but could be used if you want an message on error
        try:
            #to check if a message is a move
            def movecheck(m):
                if not m.author == player:
                    return False
                if m.content.lower() == "cancel":
                    return True
                if message_on_error:
                    return True
                # to check if a move is legal
                return board.parse_san(m.content)
            # Wait for message
            message = await bot.wait_for("message", check=movecheck)
        except asyncio.TimeoutError:
            # That awkward moment they leave you on read (You left them speechless!)
            # Basically we want to cancel the game tbf
            embed = discord.Embed(title=f"Game canceled!",
                                  description=f"{player.mention} took too long to respond.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        if message.content.lower() == "cancel":
            # If the message was cancel, then cancel...
            embed = discord.Embed(title=f"Game canceled!",
                                  description=f"{player.mention} canceled the game.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            # Delete their messages to make it a little nicer
            delete_array = [message]
            try:
                await ctx.channel.delete_messages(delete_array)
            except Exception as e:
                print(e)
                pass
            return True
        else:
            # proves if the move is possible
            if board.parse_san(message.content):
                move = board.parse_san(message.content)
                embed = discord.Embed(title=f"Move",
                                      description=f"{player.mention} moved {move.from_square} to {move.to_square}!",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                await player.send(embed=embed)
                # Make the move on the board
                board.push(move)
                # Remake the image and send it back out!
                # This is a repeat from earlier
                img = chess.svg.board(board=board)
                outputfile = open('chess_board.svg', "w")
                outputfile.write(img)
                outputfile.close()
                drawing = svg2rlg("chess_board.svg")
                renderPM.drawToFile(drawing, "chess_board.png", fmt="PNG")
                # Send the image
                await ctx.send(file=discord.File(fp="chess_board.png"))
                # Stop their turn
                turn_loop = False
            else:
                # If the move wasn't valid
                embed = discord.Embed(title=f"Error",
                                      description=f"The move you just attempted is not legal! Remember, you are whites. "
                                                  f"Please try again."
                                                  f"Or the syntax is not correct.",
                                      color=discord.Color.red())
                await player.send(embed=embed)
            # Delete the messages to make it a little nicer
            # This, again, is a copy from above
            delete_array = [message]
            try:
                await ctx.channel.delete_messages(delete_array)
            except Exception as e:
                print(e)
                pass
