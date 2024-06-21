import asyncio
from datetime import datetime
import random
from discord import app_commands
from discord.ext import commands
import discord
import youtube_dl

GUILD_ID = 520530782268162048  # Your server ID
MESSAGE_ID = 1252958696628158545  # Message ID to react to


voice_clients = []


yt_dl_opts={'format':'bestaudio/best'}
ytdl=youtube_dl.YoutubeDL(yt_dl_opts)


ffmpeg_options={'options': '-vn'}

# Dictionary mapping emojis (as strings) to role names
emoji_role_mapping = {
    "1️⃣": "huh",
    "2️⃣": "mochhuh",
    # Add more emojis and corresponding role names as needed
}

Client = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@Client.event
async def on_ready():
    print("Monaliza in action baby!")
    print("------------------------")
    try:
        synced = await Client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@Client.tree.command(name="hello",description = "Aslema Jungle!")
async def hello(interaction: discord.Interaction):
    print("Test command received")
    
    await interaction.response.send_message(
        f"Hey {interaction.user.mention}! This is Monaliza's bot!", ephemeral=True
    )

@Client.tree.command(name="khadhan",description = "Nkhodhlek chkoun?")
@app_commands.describe(member_name="chkoun nkhodh",nombre_khadhan="kadeh men khadha?")
async def khadhan(interaction : discord.Interaction , member_name : discord.Member,nombre_khadhan : int):
    ##username bech yetbadel / we need to check if user is deafning and he's in vc : done
    print("khadhan command received!")
    specific_channel_id = 1046212040756318319  # ID of the specific voice channel

    if interaction.channel.id != specific_channel_id:
        await interaction.response.send_message("You can only use this command in khadhan.", ephemeral=True)
        return

    guild = interaction.guild

    # Check if member is in a voice channel and is self-deafened
    if member_name.voice is None:
        await interaction.response.send_message(f"{member_name.display_name} is not in a voice channel.", ephemeral=True)
        return
    
    if member_name.voice.self_deaf == False:
        await interaction.response.send_message(f"{member_name.display_name} is not deafened and cannot be moved.", ephemeral=True)
        return

    initial_channel = member_name.voice.channel
    other_channels = [channel for channel in guild.voice_channels if channel != initial_channel]

    if not other_channels:
        await interaction.response.send_message("No other voice channels to move the member to.", ephemeral=True)
        return

    if nombre_khadhan <= 0:
        await interaction.response.send_message("Number of moves must be greater than zero.", ephemeral=True)
        return

    await interaction.response.send_message(f"Moving {member_name.display_name} {nombre_khadhan} times.")
    try:
        if member_name.id == 695736365513703585:
            await interaction.followup.send("3ossou rzin khodhou wahdek!")
            return
        
        if nombre_khadhan < 6:    
            for _ in range(nombre_khadhan):
                random_channel = random.choice(other_channels)
                
                await member_name.move_to(random_channel)
                await asyncio.sleep(0.5)
                
                if not member_name.voice.self_deaf:
                    break
            
            await member_name.move_to(initial_channel)
            await interaction.followup.send(f"Finished moving {member_name.display_name}.")
        else:
            await interaction.followup.send("Arkah nayek chbik ya wled!")
            await interaction.user.move_to(discord.utils.get(guild.voice_channels, name="AFK"))
    
    except Exception as e:
        print(f"Error occurred during khadhan command execution: {e}")
    



@Client.event
async def on_member_join(member):
    print(f"{member} has joined the server.")
    channel = discord.utils.get(member.guild.text_channels, name="mod-shit")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")


@Client.event
async def on_member_remove(member):
    print(f"{member} has left the server!")
    channel = discord.utils.get(member.guild.text_channels, name="mod-shit")
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
                print("Member not found!")
                return

            if guild.me.top_role <= role:
                print(
                    f"Cannot assign role '{role_name}' as it is higher or equal to the bot's top role."
                )
                return

            if not guild.me.guild_permissions.manage_roles:
                print("Bot lacks 'Manage Roles' permission.")
                return

            try:
                await member.add_roles(role)
                print(f"Assigned {role.name} to {member.display_name}")
            except discord.errors.Forbidden:
                print(
                    f"Failed to assign {role.name} to {member.display_name}. Check permissions."
                )
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
                print("Member not found!")
                return

            if guild.me.top_role <= role:
                print(
                    f"Cannot remove role '{role_name}' as it is higher or equal to the bot's top role."
                )
                return

            if not guild.me.guild_permissions.manage_roles:
                print("Bot lacks 'Manage Roles' permission.")
                return

            try:
                await member.remove_roles(role)
                print(f"Removed {role.name} from {member.display_name}")
            except discord.errors.Forbidden:
                print(
                    f"Failed to remove {role.name} from {member.display_name}. Check permissions."
                )
        else:
            print(f"Emoji {emoji} is not in the mapping.")
    else:
        print("Failed to get message or payload")


async def log_voice_state_update(member, before, after):
    log_channel = discord.utils.get(member.guild.text_channels, name="logs")
    if log_channel is None:
        print("Log channel not found!")
        return

    if not log_channel.permissions_for(member.guild.me).send_messages:
        print("Bot lacks permission to send messages in the log channel.")
        return

    embed = discord.Embed(
        title="Voice Channel Activity",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow(),
    )
    embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)

    description_parts = []

    if before.channel is None and after.channel is not None:
        description_parts.append(
            f"{member.mention} **joined** voice channel: {after.channel.mention}"
        )
        embed.add_field(name="Channel", value=after.channel.name, inline=True)
    elif before.channel is not None and after.channel is None:
        description_parts.append(
            f"{member.mention} **left** voice channel: {before.channel.mention}"
        )
        embed.add_field(name="Channel", value=before.channel.name, inline=True)
    elif before.channel is not None and after.channel is not None and before.channel.id != after.channel.id:
        description_parts.append(
            f"{member.mention} **moved** from {before.channel.mention} to {after.channel.mention}"
        )
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
        admin = await find_admin(member.guild, member, discord.AuditLogAction.member_update)
        if after.mute:
            description_parts.append(
                f"{member.mention} was **server-muted** by {admin.mention if admin else 'an admin'}."
            )
        else:
            description_parts.append(
                f"{member.mention} was **server-unmuted** by {admin.mention if admin else 'an admin'}."
            )

    if before.deaf != after.deaf:
        admin = await find_admin(member.guild, member, discord.AuditLogAction.member_update)
        if after.deaf:
            description_parts.append(
                f"{member.mention} was **server-deafened** by {admin.mention if admin else 'an admin'}."
            )
        else:
            description_parts.append(
                f"{member.mention} was **server-undeafened** by {admin.mention if admin else 'an admin'}."
            )

    if before.self_video != after.self_video:
        if after.self_video:
            description_parts.append(f"{member.mention} **opened their cam**.")
        else:
            description_parts.append(f"{member.mention} **turned off their cam**.")

    if before.self_stream != after.self_stream:
        if after.self_stream:
            description_parts.append(f"{member.mention} **started screen sharing**.")
        else:
            description_parts.append(f"{member.mention} **stopped screen sharing**.")
    embed.description = "\n".join(description_parts)

    await log_channel.send(embed=embed)


async def find_admin(guild, member, action):
    async for entry in guild.audit_logs(limit=10, action=action):
        if entry.target.id == member.id:
            return entry.user


@Client.event
async def on_voice_state_update(member, before, after):
    await log_voice_state_update(member, before, after)
#@app_commands.describe(arg = "Aslema Jungle!") chtosleh fel music part khater tekhou arguements



@Client.tree.command(name="fan", description="n7otlek fan?")
@app_commands.describe(url="lien lmusica stp")
async def fan(interaction: discord.Interaction, url: str):
    music_channel_id = 715169100456001608

    if interaction.channel.id != music_channel_id:
        return await interaction.response.send_message("You can only use this command in the music channel.", ephemeral=True)

    try:

        voice_client = await interaction.user.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client


        loop=asyncio.get_event_loop()
        data=await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if data is None:
            await interaction.response.send_message("Invalid URL or song not found.", ephemeral=True)
            return
        
        song = data[url]
        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

        voice_client.play(player)
    except Exception as e:
        print(e)
    





Client.run(
    "MTI1MjY2MTgyNjU2MzQ3NzUxNQ.GWWp0U.dnrXBLvgTheLqfJl4_aT1CHwvSpCn9XXNSiwGQ")
