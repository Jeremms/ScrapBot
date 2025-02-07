import discord
import os
import datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
import connexion
import scrapper

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Heure cible (modifier ici)
TARGET_HOUR = 11 
TARGET_MINUTE = 12

@bot.event
async def on_ready():
    print("Bot allumé !")
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

@tasks.loop(minutes=1)  # Vérifie l'heure chaque minute
async def scraping_loop():
    now = datetime.datetime.now()
    if now.hour == TARGET_HOUR and now.minute == TARGET_MINUTE:
        print("Lancement du scraping...")
        connexion.connect(os.getenv('LOG'),os.getenv('PWD'))
        data = scrapper.launch()
        channel = bot.get_channel(1337136881791537222)  # Remplace par l'ID de ton channel Discord
        if channel:
            await channel.send(f"Scraping effectué à l'heure prévue ✅ : {data}")

@bot.tree.command(name="scrap_start", description="Démarre la surveillance du scraping")
async def scrap_start(interaction: discord.Interaction):
    if scraping_loop.is_running():
        await interaction.response.send_message("Le scraping automatique est déjà en cours ⏳")
    else:
        scraping_loop.start()
        await interaction.response.send_message("Surveillance du scraping démarrée ✅")

@bot.tree.command(name="scrap_stop", description="Arrête la surveillance du scraping")
async def scrap_stop(interaction: discord.Interaction):
    if scraping_loop.is_running():
        scraping_loop.cancel()
        await interaction.response.send_message("Surveillance du scraping arrêtée ❌")
    else:
        await interaction.response.send_message("Le scraping n'était pas en cours 🚫")

bot.run(os.getenv('DISCORD_TOKEN'))
