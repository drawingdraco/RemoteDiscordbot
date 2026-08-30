import concurrent.futures
import os
import random
import time
import discord
from discord.ext import commands
import logging
import sys

##################### GAME VARIABLES #####################
#replace 'your bot token' with your actual bot token
TOKEN = 'BOT TOKEN HERE'
#####################BOT SETUP#####################
# Set up intents (required for message content access)
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'Logged in as {bot.user}')


bets = {}

##########################################################




@bot.event
async def on_message(message):
    try:
        """Called whenever a message is received."""
        # Ignore messages from the bot itself to prevent infinite loops
        if message.author == bot.user:
            return
        msg = message.content.lower()
        print(f'New message from {message.author} in {message.channel} {message.content}')

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
        try:
            if "https" in msg:
                pass
            elif msg[0] == "!":
                pass
            else:
                channel_id = 1542653273767542895
                channel = bot.get_channel(channel_id)
                if channel is None:
                    channel = await bot.fetch_channel(channel_id)
                
                if os.path.exists(str(message.author) + ".txt"):
                    with open(str(message.author) + ".txt", "r") as f:
                        existing_msg = f.read()
                        msg = int(existing_msg) + 10
                        with open(str(message.author) + ".txt", "w") as f:
                            f.write(str(msg))
                    await channel.send(f"Server points for {message.author}: {msg}")
                else:
                    with open(str(message.author) + ".txt", "w") as f:
                        f.write("10")
                    await channel.send(f"Server points for {message.author}: 10")

            ####################################
            ####################################
        except Exception as e:
            line_no = e.__traceback__.tb_lineno
            print(f"An error occurred on line: {line_no}")
            print(f"Error details: {e}")
    except Exception as e:
        print("Encountered exception: " + str(e))
    await bot.process_commands(message)

@bot.command()
async def points(ctx):
    score_file = str(ctx.author) + ".txt"
    if os.path.exists(score_file):
        with open(score_file, "r") as f:
            score = int(f.read())
    else:
        score = 0
    await ctx.send(f"Server points for {ctx.author}: {score}")

@bot.command()
async def leaderboard(ctx):
    # Get all .txt files in the current directory
    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    
    # Create a list of tuples (username, points)
    leaderboard_data = []
    for file in txt_files:
        username = file[:-4]  # Remove the .txt extension
        with open(file, 'r') as f:
            try:
                points = int(f.read())
            except ValueError:
                continue
            leaderboard_data.append((username, points))
    
    # Sort the leaderboard data by points in descending order
    leaderboard_data.sort(key=lambda x: x[1], reverse=True)
    
    # Create a formatted string for the leaderboard
    leaderboard_message = "Leaderboard:\n"
    if not leaderboard_data:
        leaderboard_message += "No scores yet."
    for rank, (username, points) in enumerate(leaderboard_data, start=1):
        leaderboard_message += f"{rank}. {username}: {points} points\n"
    
    await ctx.send(leaderboard_message)

@bot.command()
async def create_set_bet(ctx: commands.Context, bet_amount: int, bet_name: str):
    bet_attributes = {"amount": bet_amount, "creator": ctx.author, "pro": [], "contra": []}
    bet_message = await ctx.send(
        f"{ctx.author} created a bet worth {bet_amount} points. "
        "React with 👍 to bet for it or 👎 to bet against it."
    )
    bet_attributes["message_id"] = bet_message.id
    bets[bet_name] = bet_attributes
    await bet_message.add_reaction("👍")
    await bet_message.add_reaction("👎")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    for bet in bets.values():
        if bet.get("message_id") != reaction.message.id:
            continue
        if reaction.emoji == "👍" and user not in bet["pro"]:
            bet["pro"].append(user)
        elif reaction.emoji == "👎" and user not in bet["contra"]:
            bet["contra"].append(user)
        break    

@bot.command()
async def set_bet_end(ctx: commands.Context, bet_name: str, bet_winner: bool):
    if bet_name in bets:
        await ctx.send(f"The bet '{bet_name}' has ended! Here are the results:")
        bet = bets[bet_name]
        if bet_winner == True:
            winners = bet["pro"]
            losers = bet["contra"]
            await ctx.send(f"Winners: {', '.join([str(winner) for winner in winners])}")
            await ctx.send(f"Losers: {', '.join([str(loser) for loser in losers])}")
            for winner in winners:
                with open(f"{winner}.txt", "r") as f:
                    score = int(f.read())
                score += bet["amount"]
                with open(f"{winner}.txt", "w") as f:
                    f.write(str(score))
            for loser in losers:
                with open(f"{loser}.txt", "r") as f:
                    score = int(f.read())
                score -= bet["amount"]
                with open(f"{loser}.txt", "w") as f:
                    f.write(str(score))
            await ctx.send(f"Updated scores for winners and losers of the bet '{bet_name}'. Please check your scores using the !points command or the !leaderboard command.")
    else:
        await ctx.send(f"No active bet found with the name '{bet_name}'.")

@bot.command()
async def coinflip(ctx, bet_amount: int, bet_choice: str):
    if bet_choice.lower() not in ["heads", "tails"]:
        await ctx.send("Invalid choice! Please choose either 'heads' or 'tails'.")
        return

    # Simulate a coin flip
    result = random.choice(["heads", "tails"])
    await ctx.send(f"The coin landed on {result}!")

    # Update the user's score based on the result
    score_file = str(ctx.author) + ".txt"
    if os.path.exists(score_file):
        with open(score_file, "r") as f:
            score = int(f.read())
    else:
        score = 0

    if bet_choice.lower() == result:
        score += bet_amount
        await ctx.send(f"Congratulations {ctx.author}! You won {bet_amount} points.")
    else:
        score -= bet_amount
        await ctx.send(f"Sorry {ctx.author}, you lost {bet_amount} points.")

    with open(score_file, "w") as f:
        f.write(str(score))

@bot.command()
async def coinfilp(ctx, bet_amount: int, bet_choice: str):
    await ctx.send(f"User: {ctx.author}! You failed to spell coin flip correctly.")
    
if __name__ == '__main__':
    bot.run(TOKEN)
  
MESSAGE_RATE = 0.5
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
