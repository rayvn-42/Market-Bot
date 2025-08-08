import discord
from discord.ext import commands

# ========== CONFIG ==========
TOKEN = "MTI2NDc1MjMxNjk4NTExNDc2Ng.GOAz7m.mXKeuulcBCAj3K506GS2yNAyc76H56F1OSBxW4"
GUILD_ID = 1245473746429415494
MARKET_CHANNEL_NAME = "memes"
# ============================

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

async def ask_question(user, question):
    embed = discord.Embed(title="Item Creation", description=question, color=discord.Color.blue())
    msg = await user.send(embed=embed)

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)

    reply = await bot.wait_for("message", check=check)
    return reply.content.strip()

async def ask_image(user):
    embed = discord.Embed(title="Item Creation", description="Send the **Image** for the item (upload file or paste URL):", color=discord.Color.blue())
    await user.send(embed=embed)

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)
    
    msg = await bot.wait_for("message", check=check)

    if msg.attachments:
        return msg.attachments[0].url
    else:
        return msg.content.strip()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.guild is None and message.author != bot.user:  # DM only
        if message.content.lower().strip() == "add":
            user = message.author
            await user.send("Starting new item creation...")

            name = await ask_question(user, "Enter **Item Name**:")
            rarity = await ask_question(user, "Enter **Rarity**:")
            cost = await ask_question(user, "Enter **Cost** ($256 or 256):")
            image_url = await ask_image(user)
            description = await ask_question(user, "Enter **Description** (or type `skip` to leave empty):")
            if description.lower() == "skip":
                description = None

            rarity = rarity if rarity.endswith('%') else f"{rarity}%"
            cost = cost if cost.startswith('$') else f"${cost}"

            guild = bot.get_guild(GUILD_ID)
            channel = discord.utils.get(guild.text_channels, name=MARKET_CHANNEL_NAME)

            if channel:
                embed = discord.Embed(title=f"{name}", color=discord.Color.green())
                embed.add_field(name="Rarity", value=rarity if rarity.endswith('%') else rarity + '%', inline=False)
                embed.add_field(name="Cost", value=cost if cost.startswith('$') else '$'+cost, inline=False)
                embed.set_image(url=image_url)
                if description:
                    embed.add_field(name="Description", value=description, inline=False)

                await channel.send("**New item(s) in stock!**")
                await channel.send(embed=embed)
                await user.send("✅ Item posted successfully.")
            else:
                await user.send(f"❌ Could not find a channel named '{MARKET_CHANNEL_NAME}' in the server.")

    await bot.process_commands(message)

bot.run(TOKEN)
