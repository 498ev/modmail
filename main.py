import discord
from keep_alive import keep_alive
from discord.ext import commands
import random
import os
import json
from discord import Color

client = commands.Bot(command_prefix="r!", intents=discord.Intents.all())
category_id = 1288564714032336936
guild_id = 1279118022493343785
dm_message = """
Thanks for contacting support staff will assist you shortly
"""


@client.event
async def on_ready():
  print("LOGGED IN AND RUNNING")
  try:
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    activity = discord.Activity(type=discord.ActivityType.watching,
                                name="Over the Rarcade")
    await client.change_presence(status=discord.Status.dnd, activity=activity)


@client.tree.command(name="delete-ticket")
async def delete_ticket(interaction: discord.Interaction):
  if interaction.channel.category.id == category_id:
    if "closed" in interaction.channel.name:
      await interaction.channel.delete()
    else:
      await interaction.response.send_message(embed=discord.Embed(
          title="This is not closed."))
      return


@client.tree.command(name="close-ticket")
async def close_ticket(interaction: discord.Interaction):
  if interaction.channel.category.id == category_id:
    if "closed" in interaction.channel.name:
      await interaction.response.send_message(embed=discord.Embed(
          title="This is already closed."))
      return
    await interaction.channel.edit(name=f"closed-{interaction.channel.name}")


@client.event
async def on_message(message):
  if isinstance(message.channel, discord.DMChannel):
    guild = client.get_guild(guild_id)
    for c in guild.channels:
      if c.name == f"{message.author.name}":
        await c.send(f"{message.author.name}: {message.content}")
        return

    category = guild.get_channel(category_id)
    if message.author is not client.user:
      existing_channel = discord.utils.get(guild.channels,
                                           name=f"{message.author.id}")
      if existing_channel:
        await existing_channel.send(f"{message.author.name}: {message.content}"
                                    )
      else:
        ticket_channel = await guild.create_text_channel(
            f"{message.author.id}", category=category)
        overwrites = {
            guild.me:
            discord.PermissionOverwrite(read_messages=True,
                                        send_messages=True,
                                        read_message_history=True),
            guild.default_role:
            discord.PermissionOverwrite(read_messages=False),
        }
        await message.author.send(dm_message)
        await ticket_channel.edit(overwrites=overwrites)
        creation_embed = discord.Embed(
            title=
            f"{message.author.name} ({message.author.id}) has created a ticket",
            description="""
          /close-ticket (closes ticket)
          /delete-ticket (deletes ticket must be closed first)
          """)
        await ticket_channel.send(embed=creation_embed)
  else:
    if message.author.guild_permissions.ban_members and message.author.id is not client.user.id:
      try:
        member = await client.fetch_user(int(message.channel.name))
        await member.send("Support team: " + message.content)
      except:
        print("Read a message from the server (Debugger)")
  await client.process_commands(message)


client.run("MTI4ODU2NDA2NzUxMzkyOTg1MA.G4x7J-.t3k4UOVQ2uDCdHhDYEkYWI0eJFZUrPwpp9n_tU")
