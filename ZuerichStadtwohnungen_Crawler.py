import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import os
import asyncio
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler
from datetime import datetime
import hashlib

# Set up Telegram bot (replace with your bot's token and chat ID)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# URL to crawl
URL = "https://www.vermietungen.stadt-zuerich.ch/publication/apartment/"

# Set up the database path
DB_PATH = 'apartments.db'


def create_db():
    """Create a SQLite database to store listings."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apartments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT,
            rentalgross TEXT,
            rooms TEXT,
            floor TEXT,
            area TEXT,
            move_in_date TEXT,
            zone TEXT,
            link TEXT,
            timestamp TEXT,
            unique_hash TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()


def generate_unique_hash(apt):
    """Generate a unique hash for each apartment based on address, rentalgross, rooms, floor, and move_in_date."""
    unique_string = f"{apt[0]}-{apt[1]}-{apt[2]}-{apt[3]}-{apt[5]}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()


def fetch_apartments():
    """Scrape the apartment listings from the website."""
    print("Fetching apartments...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    apartments = []
    table_rows = soup.select('table tbody tr')

    for row in table_rows:
        try:
            # Extract each field, ensuring the correct class names are used
            address = row.find('td', class_='publicated_adress')
            address = address.text.strip() if address else 'Keine Angabe'

            rentalgross = row.find('td', class_='rentalgross')
            rentalgross = rentalgross.text.strip() if rentalgross else 'Keine Angabe'

            rooms = row.find('td', class_='rooms')
            rooms = rooms.text.strip() if rooms else 'Keine Angabe'

            floor = row.find('td', class_='floor')
            floor = floor.text.strip() if floor else 'Keine Angabe'

            area = row.find('td', class_='area')
            area = area.text.strip() if area else 'Keine Angabe'

            move_in_date = row.find('td', class_='move_in_date')
            move_in_date = move_in_date.text.strip() if move_in_date else 'Keine Angabe'

            zone = row.find('td', class_='metropolitan')
            zone = zone.text.strip() if zone else 'Keine Angabe'

            link = row.find('a', class_='apply_button')
            full_link = f"https://www.vermietungen.stadt-zuerich.ch{link['href']}" if link else 'No link'

            # Add all fields to the apartment tuple
            apartment = (address, rentalgross, rooms, floor, area, move_in_date, zone, full_link, str(datetime.now()))

            # Generate a unique hash for the apartment
            unique_hash = generate_unique_hash(apartment)

            apartments.append((*apartment, unique_hash))

        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    print(f"Fetched {len(apartments)} apartments.")

    # Print the first apartment's details for debugging
    if apartments:
        print("First apartment details:")
        print(apartments[0])

    return apartments


def save_new_apartments(apartments):
    """Save new apartments to the database and return newly added ones."""
    print("Saving new apartments...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    new_apartments = []

    for apt in apartments:
        cursor.execute('SELECT * FROM apartments WHERE unique_hash = ?', (apt[9],))  # Check using the unique hash
        result = cursor.fetchone()

        if result is None:
            cursor.execute(
                'INSERT INTO apartments (address, rentalgross, rooms, floor, area, move_in_date, zone, link, timestamp, unique_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                apt)  # Insert with the unique hash
            new_apartments.append(apt)
            print(f"New apartment added: {apt}")

    conn.commit()
    conn.close()

    print(f"Saved {len(new_apartments)} new apartments.")
    return new_apartments


async def send_telegram_message(app, apartment):
    """Send a new apartment listing to the Telegram channel."""
    message = (
        f"Neue Stadtwohnung gefunden am {datetime.strptime(apartment[8], '%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%Y')}:\n\n"
        f"Adresse: {apartment[0]}\n"
        f"Zone: Zürich, {apartment[6]}\n"
        f"Bruttomiete: {apartment[1]} CHF\n"
        f"Zimmer: {apartment[2]}\n"
        f"Stockwerk: {apartment[3]}\n"
        f"Fläche: {apartment[4]}\n"
        f"Vermietung ab: {apartment[5]}\n"
        f"Direktlink Bewerbung: {apartment[7]}"
    )

    retries = 3
    for _ in range(retries):
        try:
            await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            print("Message sent successfully.")
            break
        except telegram.error.TimedOut:
            print("Timed out. Retrying...")
            await asyncio.sleep(5)
    else:
        print("Failed to send message after retries")


async def main():
    create_db()

    print("Starting apartment scraper...")

    # Initialize the Telegram Application (async) with increased timeouts
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).connect_timeout(30).read_timeout(30).build()

    print("Fetching apartments...")
    apartments = fetch_apartments()
    print("Saving new apartments...")
    new_apartments = save_new_apartments(apartments)

    for apt in new_apartments:
        print(f"Sending message for apartment: {apt}")
        await send_telegram_message(app, apt)


if __name__ == "__main__":
    asyncio.run(main())
