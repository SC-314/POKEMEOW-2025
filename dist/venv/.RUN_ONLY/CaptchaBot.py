import discord
from discord.ext import commands
import nest_asyncio
from pathlib import Path


def make_embed(idx, image_url):
    '''
    Make the Embed for the artificial captcha messages
    '''
    embeds = {
        'type': 'rich',
        'title': 'A wild Captcha appeared!',
        'image': {
            'width': 246,
            'url': image_url,
            'proxy_url': image_url,
            'height': 96
        },
        'footer': {
            'text': 'You have 1 min 30s to respond correctly to the captcha image above before your account receives a ban'
        },
        'description': (
            ':exclamation: **CAPTCHA IS TEXT ONLY NOW** :exclamation: <@1115574338108801138>, '
            'you must TYPE your answer to the captcha below to continue playing!\n'
            '**(No response from the bot means you are incorrect)**\n\n'
            f'You have **{5-idx}** attempts to answer the captcha.\n'
            'Please join the [Official Support Server](https://discord.com/channels/664509279251726363/714700399239757884) '
            'and ask in <#714700399239757884> if you need help with your captcha!\n\n'
            ':exclamation: **Note**: You must have images enabled on Discord to view the image. '
            'If the image does not load, try typing an answer to refresh it (one attempt will be used).\n\n'
            ':exclamation: :exclamation: :exclamation: **TYPE your answer in the chat. '
            ':exclamation: :exclamation: :exclamation: Click on the image to view all of the numbers or letters** '
            ':exclamation: :exclamation: :exclamation:'
        ),
        'color': 15345163
    }
    return embeds

TOKEN = GUILD_ID = MSG_CHANNEL_ID = None

tokens = []
with open("./Pokemeow Bot/venv/.YOU_CAN_CHANGE/tokens.txt", 'r') as file:
    for line in file:
        tokens.append(line.replace(" ", "").strip().split("=")[1])

DISCORD_BOT_TOKEN, SERVER_ID, MSG_CHANNEL_ID = tokens[0], tokens[1], tokens[2]

TOKEN, GUILD_ID, MSG_CHANNEL_ID = DISCORD_BOT_TOKEN, SERVER_ID, MSG_CHANNEL_ID

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
image_url = 0
# Create intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

last_captcha_message = None

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} (ID: {bot.user.id})')

attempts = 0
solutions = []
image_urls = []
setup_images = []
attempts = 0
last_captcha_message = None


@bot.command()
async def setup(ctx):
    '''Set variable, get solutions, ...,  get discord links'''
    new_urls = []
    solutions = []
    folder_path = Path('./venv/.YOU_CAN_CHANGE/test_images')

    # add the solutions to a list using the image names
    for file in folder_path.iterdir():
        if file.is_file():
            solutions.append(file.name[:-4])

    # loop through the files, print the image onto discord
    # to then get the file names for the images
    for file in folder_path.iterdir():
        if file.is_file(): # get the file names
            print(f"{file}")
            file = discord.File(file)
            message = await ctx.send(file=file)
            image_url = message.attachments[0].url
            new_urls.append(image_url)
        
    # Create the string to be added to setup_data.txt
    data = ""
    for i in range(len(new_urls)):
        data += (new_urls[i] + "   " + solutions[i] + "\n")

    with open("./venv/DONT_ACCESS/setup_data.txt", 'w') as file:
        file.write(data)



@bot.command()
async def captcha(ctx):
    '''
    Captcha creating bot
    '''
    global solutions
    global attempts
    global last_captcha_message
    global image_urls
    attempts = 0

    image_urls = []
    solutions = []

    # download the the image and solutions using setup_data.txt
    with open('./venv/DONT_ACCESS/setup_data.txt') as file:
        for line in file:
            data_list = line.strip().split("   ")
            image_urls.append(data_list[0])
            solutions.append(data_list[1])

    if len(solutions) < 5:
        await ctx.send("you need more images in the test_images folder, remember to use !setup after adding the new images")
        return None
    
    
    last_captcha_message = await ctx.send(embed=discord.Embed.from_dict(make_embed(attempts, image_urls[attempts])), reference=ctx.message)

    content = "Here is your CAPTCHA!"
    print(solutions)


@bot.event
async def on_message(message):
    '''
    Check if the responce is good or not'''
    global MSG_CHANNEL_ID
    global last_captcha_message
    global attempts
    global solutions

    if message.author.bot:
        return
    

    # Debug: Print the content of the received message
    print(f'Message received: {message.content} in channel: {message.channel.id}')

    # Check if the message is in the channel where the CAPTCHA was sent
    if (str(message.channel.id) == str(MSG_CHANNEL_ID)) and last_captcha_message != None:
        
        print("debug point 1")
        print(solutions)
        if attempts == 4:
            if last_captcha_message:
                await last_captcha_message.edit(content="You are banned for 30 minutes", embed=None)
                last_captcha_message = None
                attempts = 0

        elif message.content == solutions[attempts]:
            if last_captcha_message:
                await last_captcha_message.edit(content="Thank you, you may continue playing!", embed=None)
                last_captcha_message = None
                attempts = 0

        else:
            if last_captcha_message:
                attempts += 1
                print(image_url)
                await last_captcha_message.edit(embed=discord.Embed.from_dict(make_embed(attempts, image_urls[attempts])))


    # Process commands if applicable
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)