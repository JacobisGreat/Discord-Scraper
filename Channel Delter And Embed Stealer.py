import discord
import asyncio
import json
import os

token = input("Whats yo token nigga: ")
client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    print('Ready to listen for commands.')

@client.event
async def on_message(message):
    if message.author == client.user:
        if message.content.startswith("!fetch"):
            message_link = message.content.split(" ")[1]
            await fetch_embed(message, message_link)
        elif message.content == ".":
            await delete_channel(message.channel)

async def fetch_embed(message, message_link):
    try:
        # Extract channel_id and message_id from the message link
        parts = message_link.split('/')
        channel_id = int(parts[-2])
        message_id = int(parts[-1])

        channel = client.get_channel(channel_id)
        if not channel:
            await message.channel.send("Channel not found.")
            return

        msg = await channel.fetch_message(message_id)
        if not msg:
            await message.channel.send("Message not found.")
            return

        if not msg.embeds:
            await message.channel.send("No embeds found in the message.")
            return

        # Remove the 'type', 'proxy_url', 'width', and 'height' keys from each embed
        embed_data = [remove_excess_keys(embed.to_dict()) for embed in msg.embeds]
        json_data = json.dumps({"embeds": embed_data}, indent=4)

        # Send the JSON data as a file
        file_path = os.path.abspath('embed_data.json')
        with open('embed_data.json', 'w') as file:
            file.write(json_data)

        await message.channel.send(file=discord.File('embed_data.json'))
        os.remove(file_path)  # Clean up the file after sending

    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")

def remove_excess_keys(embed_dict):
    # Remove keys that might cause issues
    keys_to_remove = ['type', 'proxy_url', 'width', 'height']
    for key in keys_to_remove:
        if key in embed_dict:
            del embed_dict[key]
        if 'image' in embed_dict and key in embed_dict['image']:
            del embed_dict['image'][key]
    return embed_dict

async def delete_channel(channel):
    try:
        await channel.delete()
        print(f'Channel {channel.name} deleted.')
    except Exception as e:
        print(f"An error occurred while deleting the channel: {e}")

client.run(token)