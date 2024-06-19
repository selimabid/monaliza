import discord
from discord.ext import commands
from datetime import datetime

GUILD_ID = 1252689693804462252  # Your server ID
MESSAGE_ID = 1252701957299376302  # Message ID to react to

# Dictionary mapping emojis (as strings) to role names
emoji_role_mapping = {
    "1️⃣": "Role1",
    "2️⃣": "Role2",
    # Add more emojis and corresponding role names as needed
}

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@Client.event
async def on_ready():
    print("Monaliza in action baby!")
    print("------------------------")

@Client.command()
async def hello(ctx):
    print("Test command received")  
    await ctx.send("Hello, this is Monaliza's Bot!")

@Client.event
async def on_member_join(member):
    print(f"{member} has joined the server.")
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

@Client.event
async def on_member_remove(member):
    print(f"{member} has left the server!")
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Baslema, {member.mention}!")

@Client.event
async def on_raw_reaction_add(payload):
    print(f"Message ID: {payload.message_id}, Emoji: {str(payload.emoji)}")
    
    if payload.message_id == MESSAGE_ID:
        emoji = str(payload.emoji)
        guild = Client.get_guild(GUILD_ID)
        
        if guild is None:
            print("Server not found!")
            return

        if emoji in emoji_role_mapping:
            role_name = emoji_role_mapping[emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            
            if role is None:
                print(f"Role '{role_name}' not found!")
                return

            member = guild.get_member(payload.user_id)
            
            if member is None:
                print ("Member not found!")
                return

            if guild.me.top_role <= role:
                print(f"Cannot assign role '{role_name}' as it is higher or equal to the bot's top role.")
                return

            if not guild.me.guild_permissions.manage_roles:
                print("Bot lacks 'Manage Roles' permission.")
                return

            try:
                await member.add_roles(role)
                print(f"Assigned {role.name} to {member.display_name}")
            except discord.errors.Forbidden:
                print(f"Failed to assign {role.name} to {member.display_name}. Check permissions.")
        else:
            print(f"Emoji {emoji} is not in the mapping.")
    else:
        print("Failed to get message or payload")

@Client.event
async def on_raw_reaction_remove(payload):
    print(f"Message ID: {payload.message_id}, Emoji: {str(payload.emoji)}")
    
    if payload.message_id == MESSAGE_ID:
        emoji = str(payload.emoji)
        guild = Client.get_guild(GUILD_ID)
        
        if guild is None:
            print("Server not found!")
            return

        if emoji in emoji_role_mapping:
            role_name = emoji_role_mapping[emoji]
            role = discord.utils.get(guild.roles, name=role_name)
            
            if role is None:
                print(f"Role '{role_name}' not found!")
                return

            member = guild.get_member(payload.user_id)
            
            if member is None:
                print ("Member not found!")
                return

            if guild.me.top_role <= role:
                print(f"Cannot remove role '{role_name}' as it is higher or equal to the bot's top role.")
                return

            if not guild.me.guild_permissions.manage_roles:
                print("Bot lacks 'Manage Roles' permission.")
                return

            try:
                await member.remove_roles(role)
                print(f"Removed {role.name} from {member.display_name}")
            except discord.errors.Forbidden:
                print(f"Failed to remove {role.name} from {member.display_name}. Check permissions.")
        else:
            print(f"Emoji {emoji} is not in the mapping.")
    else:
        print("Failed to get message or payload")







@Client.event
async def on_voice_state_update(member, before, after):
    log_channel = discord.utils.get(member.guild.text_channels, name="logs")  # Ensure 'logs' is the correct channel name
    if log_channel is None:
        print("Log channel not found!")
        return

    if not log_channel.permissions_for(member.guild.me).send_messages:
        print("Bot lacks permission to send messages in the log channel.")
        return

    embed = discord.Embed(title="Voice Channel Activity", color=discord.Color.blue(), timestamp=datetime.utcnow())
    embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    
    description_parts = []

    if before.channel is None and after.channel is not None:
        description_parts.append(f"{member.mention} **joined** voice channel: {after.channel.mention}")
        embed.add_field(name="Channel", value=after.channel.name, inline=True)
    elif before.channel is not None and after.channel is None:
        description_parts.append(f"{member.mention} **left** voice channel: {before.channel.mention}")
        embed.add_field(name="Channel", value=before.channel.name, inline=True)
    elif before.channel is not None and after.channel is not None and before.channel.id != after.channel.id:
        description_parts.append(f"{member.mention} **moved** from {before.channel.mention} to {after.channel.mention}")
        embed.add_field(name="Old Channel", value=before.channel.name, inline=True)
        embed.add_field(name="New Channel", value=after.channel.name, inline=False)

    if before.self_mute != after.self_mute:
        if after.self_mute:
            description_parts.append(f"{member.mention} **self-muted**.")
        else:
            description_parts.append(f"{member.mention} **self-unmuted**.")

    if before.self_deaf != after.self_deaf:
        if after.self_deaf:
            description_parts.append(f"{member.mention} **self-deafened**.")
        else:
            description_parts.append(f"{member.mention} **self-undeafened**.")

    if before.mute != after.mute:
        if after.mute:
            description_parts.append(f"{member.mention} was **server-muted** by an admin.")
        else:
            description_parts.append(f"{member.mention} was **server-unmuted** by an admin.")

    if before.deaf != after.deaf:
        if after.deaf:
            description_parts.append(f"{member.mention} was **server-deafened** by an admin.")
        else:
            description_parts.append(f"{member.mention} was **server-undeafened** by an admin.")

    embed.description = "\n".join(description_parts)

    await log_channel.send(embed=embed)



Client.run("MTI1MjY2MTgyNjU2MzQ3NzUxNQ.GWWp0U.dnrXBLvgTheLqfJl4_aT1CHwvSpCn9XXNSiwGQ")
