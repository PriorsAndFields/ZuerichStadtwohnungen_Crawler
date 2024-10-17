# 🏢 Zürich Stadtwohnung Crawler - Automating Zürich Apartment Listings

## TL;DR
This is a fully automated web scraper for fetching apartment listings from Zürich’s public real estate portal. Powered by **Python**, **SQLite**, and **Telegram**, it continuously monitors the latest listings, updates a local database, and fires off notifications to this dedicated Telegram channel https://t.me/ZurichStadtwohnungenNeu. Set up as a cron job, this bot runs on autopilot and is easily extendable. Open-source, highly modular, and ready for your own customizations.

For more details about the source of the listings and rental guidelines, please visit the official website of the City of Zurich at www.stadt-zuerich.ch/e-vermietung.

### Why?
Because manually refreshing a real estate site is for mere mortals.

## 🔧 Tech Stack
- **Python 3.8+**: Core runtime.
- **SQLite**: The lightweight DB for storing listings.
- **BeautifulSoup**: Efficient HTML parsing and scraping.
- **Selenium**: Because dynamic JavaScript elements are a pain.
- **Telegram Bot API**: Shoot apartment updates directly into a channel. Instantaneous feedback, with no polling required.
- **Linux cron**: Schedule, automate, and forget.

## 🧠 What This Script Actually Does
The script automatically:
1. **Scrapes Zürich apartment listings** from the official website every 15-30 minutes.
2. **Processes and cleans the data**, parsing essential information like:
    - **Address**
    - **Number of Rooms**
    - **Gross Rent**
    - **Floor & Area**
    - **Move-in Date**
    - **Zone** (District)
    - **Direct Application Link**
3. **Stores the data** in a local SQLite database for reference, preventing duplicate postings.
4. **Pushes updates** to a Telegram channel, letting followers know about the latest apartments as soon as they’re posted.

### The Devil's in the Details
- Each scraped listing is compared against existing data in the SQLite database to avoid duplicates. I use a distinct combination of address, rent, and room count to ensure that each apartment listing is unique.
- The script handles missing info gracefully and logs issues, so you can adjust as needed.
- Built-in retry logic ensures that failed attempts (due to server or connection hiccups) don’t disrupt the workflow.

## 🚀 Setting It Up
### Clone the Repository
```bash
git clone https://github.com/yourusername/stadtwohnung-crawler.git
cd stadtwohnung-crawler
```

### Install Dependencies
Ensure you’re running Python 3.8+ and install the necessary Python packages:
```bash
pip install -r requirements.txt
```

### Configuration
To avoid publishing sensitive data (like Telegram bot tokens), I leverage environment variables or store them in a `.env` file. Set up your Telegram bot credentials:
```bash
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
TELEGRAM_CHAT_ID = 'your-telegram-channel-id'
```

### Database
You don't need to worry about manually setting up a database. The script will auto-generate an SQLite database (`apartments.db`) on its first run.

### Running the Script
You can test the scraper with:
```bash
python3 TryAlpha1.py
```

### Automating with Cron
Run the script every 15 minutes (or whatever interval suits your needs). Here’s the magic line to add to your cron setup:
```bash
*/15 * * * * /path/to/your/env/bin/python /home/ubuntu/scripts/TryAlpha1.py
```

## ⚙️ How It Works - Under the Hood
1. **Web Scraping**: BeautifulSoup extracts apartment listings from static HTML, while Selenium is there to handle dynamic content when JavaScript gets in the way.
2. **Database**: New apartment listings get written into SQLite. We track each unique listing by address, rent, and room count—ensuring that only fresh listings get posted.
3. **Notifications**: Via the Telegram API, each new apartment listing is formatted and sent to your designated channel.
4. **Error Handling & Logs**: Gotcha moments (like connection timeouts or weird HTML structures) are handled gracefully, with logs detailing anything out of the ordinary.

## 📦 Project Files
- **`ZuerichStadtwonungen_Crawler.py`**: The Python script that orchestrates scraping, storing, and posting to Telegram.
- **`requirements.txt`**: (will be uploaded later) Contains all the Python dependencies. Use this to get the exact same setup locally or on a server.
- **`apartments.db`**: (will be uploaded later) SQLite database that’s created and updated automatically during the scraping process.
- **`.gitignore`**: (will be uploaded later) Because you don’t want to accidentally push sensitive tokens or database files to GitHub.
- **`README.md`**: This file—an overview of the project and how to use it.

## 💡 Customization & Extensibility
- Want more fields? No problem. The script is modular. You can extend the scraping logic to include additional apartment info or even monitor different cities or property types.
- Planning on scaling this? Swap out SQLite for a full-fledged database (like PostgreSQL) with minimal refactoring.
- Need to support multiple Telegram channels? Easy—duplicate the Telegram posting logic and modify as needed.

## 🌍 Contributing
Fork this repo, add your secret sauce, and submit a PR. This is open-source and I'm always down for new ideas, improvements or bug fixes.

### Contribution Process:
1. Fork the repository.
2. Clone it locally.
3. Create a new feature branch (`git checkout -b feature-branch`).
4. Commit your changes.
5. Push to your branch and create a Pull Request.

## 📝 License
MIT License. Use it, modify it, redistribute it—just give credit where it’s due.
