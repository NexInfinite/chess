# This bot was originally an order from fiverr but they guy never paid and i thought it was pretty cool so here it is! If you need any help message me. Please not I am very very bad at naming variables!

# For a little bit of back story. This guy wanted me to make this bot and i said yes, started making then he said "Can you turn it into pokecord".
# At first i was skeptical but i decided to ask for the price. He wouldn't change the price and tried to get me to make a huge bot in a couple months paying me $60.
# Of course i said no as it was a huge job and that pay is pretty bad (seeing as fiverr takes 20%). He then kept saying he was gonna pay me then changing things around.
# In the end he blocked me, and i thought that people may want this bot so here it is. Enjoy! If you ever do commissions do not start until they have paid!
# This is a rule i ignored and well, bruh moment. lol

# import all needed imports
import datetime
import sys
import traceback

import discord
from discord.ext import commands

TOKEN = "YOUR TOKEN HERE"  # Test build
bot = commands.Bot(command_prefix="c!", case_insensitive=True)  # Description for bot help command
# Load Cog
startup_extensions = ["Cog.help", "Cog.chess"]


@bot.event
async def on_ready():
    # On read, after startup
    print(f"Connecting...\nConnected {bot.user}")  # Send message on connected

# Below is error handling. You dont need to worry about it but feel free to contact me to talk about it. I did not make this and i use someone else's code. Here's a link: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612


@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
        embed = discord.Embed(title=f"{ctx.command} error",
                              description='I need the **{}** permission(s) to run this command.'.format(fmt),
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description="This command has been disabled",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandOnCooldown):
        remaining = "{}".format(str(datetime.timedelta(seconds=error.retry_after)))
        embed = discord.Embed(title=f"Click here to vote",
                              description=f"This command is on cooldown, please try again in "
                                          f"{remaining[0:1]} hours, "
                                          f"{remaining[3:4]} minutes, "
                                          f"{remaining[6:7]} seconds!\n"
                                          f"To avoid getting these cooldowns please vote by clicking above! This will "
                                          f"kick in within 1 minute and 30 seconds!",
                              url="https://top.gg/bot/700793365754806402/vote",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, discord.HTTPException):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"Sadly I could not send a message. This can be because it was too long or "
                                          f"it didnt form a url correctly. Check below to see the real error!",
                              color=discord.Color.red())
        embed.set_footer(error)
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"{_message}",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandError):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"Invalid user input. "
                                          f"Please use `{bot.command_prefix}help {ctx.command.cog_name}` "
                                          f"and locate the `{ctx.command}` command. Check what arguments are "
                                          f"needed underneath it and retry this command!",
                              color=discord.Color.red())
        embed.set_footer(text=f"Debug error message: {error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.UserInputError):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"Invalid user input. "
                                          f"Please use `{bot.command_prefix}help {ctx.command.cog_name}` "
                                          f"and locate the `{ctx.command}` command. Check what arguments are "
                                          f"needed underneath it and retry this command!",
                              color=discord.Color.red())
        embed.set_footer(text=f"Debug error message: {error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            embed = discord.Embed(title=f"{ctx.command} error",
                                  description="This command cannot be sued in direct messages",
                                  color=discord.Color.red())
            embed.set_footer(text=f"{error}")
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"You do not have permission to use this command",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    # ignore all other exception types, but print them to stderr
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


if __name__ == "__main__":  # When script is loaded, this will run
    bot.remove_command("help")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)  # Loads cogs successfully
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))  # Failed to load cog, with error

bot.run(TOKEN)  # Run bot with token
