import concurrent.futures
import random
import keyboard
import pydirectinput
import pyautogui

from Discord_remote_KeyCodes import *
import discord
##################### GAME VARIABLES #####################
#replace 'your bot token' with your actual bot token
TOKEN = 'your bot token'
#####################BOT SETUP#####################

# Set up intents (required for message content access)
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'Logged in as {client.user}')

##########################################################


@client.event
async def on_message(message):
    try:
        """Called whenever a message is received."""
        # Ignore messages from the bot itself to prevent infinite loops
        if message.author == client.user:
            return
        msg = message.content.lower()
        print(f'New message from {message.author} in {message.channel}: {message.content}')

        # Now that you have a chat message, this is where you add your  logic.
        # Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
        # Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
        # Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
        # Use the pydirectinput library to press or move the mouse

        #some example videogame logic code below:

        ###################################
        # Example Code 
        ###################################

        # If the chat message is "left", then hold down the A key for 2 seconds
        if msg == "left": 
            HoldAndReleaseKey(A, 2)

        # If the chat message is "right", then hold down the D key for 2 seconds
        if msg == "right": 
            HoldAndReleaseKey(D, 2)

        # If message is "forward", then permanently hold down the W key
        if msg == "forward": 
            ReleaseKey(S) #release brake key first
            HoldKey(W) #start permanently driving

        # If message is "reverse", then permanently hold down the S key
        if msg == "reverse": 
            ReleaseKey(W) #release forward key first
            HoldKey(S) #start permanently reversing

        # Release both the "forward" and "reverse" keys
        if msg == "stop": 
            ReleaseKey(W)
            ReleaseKey(S)

        # Press the spacebar for 0.7 seconds
        if msg == "jump": 
            HoldAndReleaseKey(SPACE, 0.7)

        # Move the mouse up by 30 pixels
        if msg == "aim up":
            pydirectinput.moveRel(0, -30, relative=True)

        # Move the mouse right by 200 pixels
        if msg == "aim right":
            pydirectinput.moveRel(200, 0, relative=True)

        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))

if __name__ == '__main__':
    client.run(TOKEN)
  
MESSAGE_RATE = 0.5
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

