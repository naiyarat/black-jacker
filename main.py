import discord
from dotenv import load_dotenv
import random
import os
import time

from discord.ext import commands

load_dotenv()
TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()

intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)
BACKSHOT = 'https://tenor.com/view/gojo-satoru-gif-14818873849943523300'
AKANE = 'https://tenor.com/view/oshi-no-ko-oshi-no-ko-reaction-anime-anime-reaction-happy-gif-11489210881418844148'
DORAEMON_CRYING = 'https://tenor.com/view/reupload-doraemon-doraemon-angry-gif-3795486608840357480'
DORAEMON_HAPPY = 'https://tenor.com/view/doraemon-cartoon-snacks-reupload-gif-657361926656401994'
SHUFFLE = 'https://tenor.com/view/cards-card-trick-shuffle-card-game-how-to-shuffle-gif-22218157'
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    
@client.command()
async def usage(ctx: commands.Context):
    help_message = """
    **------------------------Usage------------------------**

    **!blackjack**
    Starts a game of Blackjack. You'll receive two cards and can choose to "hit" (draw another card) or "stand" (end your turn). The bot will then play as the dealer. Try to get as close to 21 without going over!

    **!rules**
    Gives an explaination of how to play Blackjack, albiet a bit simplified
    
    **!end**
    Ends the gambling...

    **Game Tips:**
    1) Type **hit** to draw another card during your turn.
    2) Type **stand** to end your turn and let the dealer play.
    3) Type **quit** at any time during the game to exit early.
    """
    await ctx.send(help_message)
    
@client.command()
async def rules(ctx: commands.Context):
    rules_message = """
    **------------------------Rules------------------------**

    **Objective**: The goal is to have a hand value as close to **21** as possible, without going over (busting).
    
    **Card Values**:
    1) Number cards (2-10) are worth their face value.
    2) Face cards (Jack, Queen, King) are each worth **10**.
    3) Aces can be worth **11** or **1**, depending on which is more beneficial.

    **Gameplay**:
    1) At the start of each round, both you (the player) and the dealer receive two cards.
    2) Your cards are visible to you, while the dealer reveals only one card at first.
    3) You can choose to **hit** (draw a card) or **stand** (end your turn).
    4) The goal is to reach 21 or as close as possible without going over.
    
    **Winning**:
    1) If your hand exceeds **21**, you bust, and the dealer wins automatically.
    2) If you stand and the dealer busts by going over 21, you win.
    3) If both you and the dealer stay under 21, the hand with the higher total wins.
    4) If you both have the same total, it's a **draw**.

    **Blackjack**:
    1) If your starting hand equals **21** (e.g., an Ace and a 10 or face card), you have **Blackjack** and win instantly unless the dealer also has Blackjack, resulting in a draw.

    Happy gambling!
    """
    await ctx.send(rules_message)

    
@client.command()
async def blackjack(ctx: commands.Context):
    async def say(msg):
        await ctx.send(msg)
        time.sleep(1)         

    await say("Let's start the game!")
    await say("Shuffling deck...")
    
    categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
    cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] 
    deck = [(card, category) for category in categories for card in cards]
    
    random.shuffle(deck)
    await say(SHUFFLE)
    
    while len(deck) > 4:  
        player_card = [deck.pop(), deck.pop()] 
        dealer_card = [deck.pop(), deck.pop()] 

        player_score = sum(card_value(card) for card in player_card) 
        dealer_score = sum(card_value(card) for card in dealer_card) 
        time.sleep(2)
        await say("**------------------------New Round! Drawing Cards------------------------**")
        
        await say(f"Your cards: **{', '.join(f'{rank} of {suit}' for rank, suit in player_card)}**")
        await say(f"Your score: **{player_score}**") 
        
        # user's turn
        while True:
            if player_score == 21:
                await say("Wow! **Blackjack**! :speaking_head: :speaking_head: :speaking_head: :fire: :fire: :fire: :bangbang: :bangbang: :bangbang:")
                await say(AKANE)
                break
            if len(deck) == 0:
                await say("No cards left in the deck! You have to **STAND**!")
                break
            await say('Would you like to **HIT** or **STAND**?')
            msg = await client.wait_for(
                'message',
                check=lambda message: message.author == ctx.author and message.content.lower() in ["hit", "stand"],
            )
            if 'stand' in msg.content.lower(): 
                await say("You **STAND**! It's my turn..")
                break
            elif 'quit' in msg.content.lower():
                await say("Until next time!") 
                return
            elif 'hit' in msg.content.lower():
                await say("You **HIT**! Let's see what you get..")
                
                new_card = deck.pop()
                player_card.append(new_card) 
                player_score += card_value(new_card)
                
                await say(f"You got **{new_card[0]} of {new_card[1]}**")
                await say(f"Your cards: **{', '.join(f'{rank} of {suit}' for rank, suit in player_card)}**")
                await say(f"Your score: **{player_score}**") 
                
                if player_score > 21: 
                    await say("**BUST**! I **WIN**! Your score exceeds **21**!") 
                    await say(AKANE)
                    break
                
        if player_score > 21: 
            continue
        # dealer's turn
        await say("**------------------------Dealer's Turn------------------------**")
        await say("Revealing my cards..")
        await say(f"I have: **{', '.join(f'{rank} of {suit}' for rank, suit in dealer_card)}**")
        await say(f"My score: **{dealer_score}**")
        if dealer_score == 21:
            await say("Wow! **Blackjack**! :speaking_head: :speaking_head: :speaking_head: :fire: :fire: :fire: :bangbang: :bangbang: :bangbang:")
            await say(AKANE)
        
        if dealer_score > player_score:
            await say(f"Didn't even have to draw! I **WIN** **{dealer_score}** to **{player_score}**!")
            await say(BACKSHOT)
        
        elif dealer_score < player_score:
            while dealer_score < random.randint(16, 18) or dealer_score < player_score:
                if len(deck) > 0:
                    await say("I'll **HIT**! Let's see what I get..")
                    new_card = deck.pop()
                    dealer_card.append(new_card)
                    dealer_score += card_value(new_card)
                    await say(f"I got **{new_card[0]} of {new_card[1]}**")
                    await say(f"My cards: **{', '.join(f'{rank} of {suit}' for rank, suit in dealer_card)}**")
                    await say(f"My score: **{dealer_score}**") 
                if dealer_score > 21: 
                    await say("**BUST**! Crap you **WIN**! My score exceeds **21**!")
                    await say(DORAEMON_CRYING) 
                    await say()
                    break
                elif dealer_score > player_score:
                    await say(f"You are a$$! I **WIN** **{dealer_score}** to **{player_score}**!")
                    await say(DORAEMON_HAPPY)
                    break
                elif dealer_score == player_score:
                    await say(f"It's a **DRAW**! I'll take it.")
                    break
                elif dealer_score < player_score and len(deck) == 0:
                    await say(f"I **LOST**! What a fluke!")
                    await say(DORAEMON_CRYING) 
                time.sleep(2)
    await say("We are out of cards! Thanks for playing.")
    return
        
@client.command()
async def end(ctx: commands.Context):
   await ctx.send('Never stop gambling! Gamble on!')
   await ctx.send(BACKSHOT)
                    
def card_value(card, score=None): 
    if card[0] in ['Jack', 'Queen', 'King']: 
        return 10
    elif card[0] == 'Ace':
        # Check if score is defined and if adding 11 would cause a bust
        if score is not None and score + 11 > 21:
            return 1
        return 11
    else:
        return int(card[0])
    
client.run(TOKEN)