import discord
from discord.ext import commands
from credentials import DISCORD_BOT_TOKEN
from firewall.main import FirewallManager

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$gcp ", intents=intents)

fw = FirewallManager()

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")

@bot.command()
async def add_ip(ctx, ip: str):
    if fw.add_ip(ip):
        await ctx.send(f"Added IP: {ip}")
    else:
        await ctx.send(f"Failed to add IP: {ip}")

@bot.command()
async def remove_ip(ctx, ip: str):
    if fw.remove_ip(ip):
        await ctx.send(f"Removed IP: {ip}")
    else:
        await ctx.send(f"Failed to remove IP: {ip}")

@bot.command()
async def list_ips(ctx):
    ips = fw.list_ips()

    message = ''

    for ip in ips:
        message += f'- {ip}\n'

    await ctx.send(message)

def start_server():
    bot.run(DISCORD_BOT_TOKEN)

def main():
    start_server()

if __name__ == '__main__':

    main()