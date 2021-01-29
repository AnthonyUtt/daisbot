import discord
from discord.ext import commands
import random
import re
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description='A simple TTRPG helper bot', intents=intents)

# Helper functions
def roll_die(arg: str):
    m = re.match("(\d+)d(\d+)\s?(\+|\-)?\s?(\d+)?", arg)
    try:
        num = m.group(1)
        die = m.group(2)
        sign = m.group(3)
        mod = m.group(4)

        rolls = [random.randint(1, int(die)) for i in range(int(num))]
        total = sum(rolls) + (int(sign + mod) if mod is not None else 0)
        return [rolls, sign, mod, total]
    except:
        return

def roll_dice(iter: int, arg: str):
    return [roll_die(arg) for i in range(iter)]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def roll(ctx, arg:str='1d20'):
    t = roll_die(arg)
    if t:
        await ctx.send('Rolling %s: (%s)%s%s = %d' % (arg, ', '.join([str(r) for r in t[0]]), ((' %s' % t[1]) if t[1] is not None else ''), ((' %s' % t[2]) if t[2] is not None else ''), t[3]), mention_author=True)
    else:
        await ctx.send('Invalid arguments!', mention_author=True)
    return

@bot.command()
async def r(ctx, arg:str='1d20'):
    await roll(ctx, arg)

@bot.command()
async def roll_many(ctx, i: int, arg: str):
    rolls = roll_dice(i, arg)
    if len(rolls) > 0:
        msg = '\n'.join(['Rolling %s: (%s)%s%s = %d' % (arg, ', '.join([str(r) for r in t[0]]), ((' %s' % t[1]) if t[1] is not None else ''), ((' %s' % t[2]) if t[2] is not None else ''), t[3]) for t in rolls])
        msg += ('\nTotal: %d' % (sum([t[3] for t in rolls])))
        await ctx.send(msg, mention_author=True)
    else:
        await ctx.send('Invalid arguments!', mention_author=True)

@bot.command()
async def rr(ctx, i: int, arg: str):
    await roll_many(ctx, i, arg)

@bot.command()
async def advantage(ctx, arg:str='+0'):
    m = re.match("((\+|\-)\d+)", arg)
    try:
        mod = m.group(1)
        rolls = roll_dice(2, '1d20' + mod)

        if len(rolls) > 0:
            msg = 'Rolling 1d20%s with advantage:\n' % (arg)
            msg += '\n'.join(['Roll %d: (%s)%s%s = %d' % (i + 1, ', '.join([str(r) for r in t[0]]), ((' %s' % t[1]) if t[1] is not None else ''), ((' %s' % t[2]) if t[2] is not None else ''), t[3]) for (i, t) in enumerate(rolls)])
            msg += ('\nResult: %d' % (max([t[3] for t in rolls])))
            await ctx.send(msg, mention_author=True)
        else:
            await ctx.send('Invalid arguments!', mention_author=True)
    except:
        await ctx.send('Invalid arguments!', mention_author=True)

@bot.command()
async def disadvantage(ctx, arg:str='+0'):
    m = re.match("((\+|\-)\d+)", arg)
    try:
        mod = m.group(1)
        rolls = roll_dice(2, '1d20' + mod)

        if len(rolls) > 0:
            msg = 'Rolling 1d20%s with disadvantage:\n' % (arg)
            msg += '\n'.join(['Roll %d: (%s)%s%s = %d' % (i + 1, ', '.join([str(r) for r in t[0]]), ((' %s' % t[1]) if t[1] is not None else ''), ((' %s' % t[2]) if t[2] is not None else ''), t[3]) for (i, t) in enumerate(rolls)])
            msg += ('\nResult: %d' % (min([t[3] for t in rolls])))
            await ctx.send(msg, mention_author=True)
        else:
            await ctx.send('Invalid arguments!', mention_author=True)
    except:
        await ctx.send('Invalid arguments!', mention_author=True)

@bot.command()
async def adv(ctx, arg:str='+0'):
    await advantage(ctx, arg)

@bot.command()
async def disadv(ctx, arg:str='+0'):
    await disadvantage(ctx, arg)

bot.run(os.getenv('TOKEN'))