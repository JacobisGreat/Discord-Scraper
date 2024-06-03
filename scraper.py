import discord

token = input("Whats yo token: ")
client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await save_channel_ids()

async def save_channel_ids():
    channel_ids = []
    for guild in client.guilds:
        print(f"Checking guild: {guild.id} - {guild.name}")
        if guild.id == 1243324188459008010:
            # Exception guilds here
            print("Not allowed to scrape this guild:", guild.id)
            continue  # Skip this guild
        for channel in guild.text_channels:
            permissions = channel.permissions_for(guild.me)
            if permissions.send_messages:
                channel_ids.append(f"\"{channel.id}\",")
                print(f"Added channel: {channel.id} - {channel.name} from guild: {guild.id}")

    with open('channel_ids.txt', 'w') as file:
        file.write('\n'.join(channel_ids))

    print('Channel IDs saved to channel_ids.txt')

client.run(token)
