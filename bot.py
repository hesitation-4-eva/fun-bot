import discord, random, os, gfycat
import json
from gfycat.client import GfycatClient
from discord.ext import commands
with open('apis.json', 'r') as apis:
    json_dict = json.load(apis)
path_to_images = json_dict["images"]

disclient = commands.Bot(command_prefix = '.')


@disclient.command(aliases=['stop!'])
async def stop(ctx):
    await ctx.send("stopping bot!")
    

@disclient.command(aliases=['inputs'])
async def folder_list(ctx):
    to_send = os.listdir(path_to_images)
    await ctx.send('```' + str(to_send) + '```')  # send a list of available inputs for fap command


@disclient.command(aliases=['random'])
async def send_thing(ctx):
    paths = []
    for directory in os.listdir(path_to_images):
        paths.append(directory)  # append these directories to the list paths

    alpha = random.choice(paths)  # pick a random path out of the list
    beta = os.listdir(path_to_images + alpha + '/') 
    beta_refined = []  # list contains all of the images in the path
    for images in beta:
        if ".mp4" not in images and ".ini" not in images and os.stat(path_to_images + alpha + '/' + images).st_size < 800 * 1000:
            beta_refined.append(images)  # appends all of the images to the list

    gamma = random.choice(beta_refined)  # picks a random image from the path
    delta = path_to_images + alpha + '/' + gamma
    print("Send out " + delta)
    await ctx.send(file= discord.File(delta))


@disclient.command(aliases=['fap'])
async def send_specified(ctx, input, filetype='.jpg', number=5):  # define some params so user does not need to enter
    if not input:
        return await ctx.send("No name given, please input a name after command")

    user_wants = path_to_images + str(input) + '/'
    files_list = []
    if os.path.exists(user_wants):
        for files in os.listdir(user_wants):
            if files.endswith(filetype) and os.stat(user_wants + files).st_size < 8000 * 1024:
                files_list.append(files)
        print(len(files_list))         
    else:
        print("Path doesn't exist!")
        await ctx.send("Nothing for " + input)

    for _ in range(int(number)):
        choice = random.choice(files_list)
        send_out = user_wants + choice
        print("Sent out " + send_out)
        await ctx.send(file= discord.File(send_out))
        files_list.remove(choice)
        

@disclient.event
async def on_ready():
    await disclient.change_presence(status= discord.Status.online)
    print("bot is online!")


disclient.run(json_dict["discord_token"])

gfyclient = GfycatClient(json_dict["client_id"], json_dict["client_secret"])
