# AMD-Auto-File-Rename-Bot

A Telegram bot for auto-renaming files with metadata preservation.

#Telegram bot for auto-rename-bot

### Method 1: Using Render Blueprint (Recommended)
1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Click "Apply" on the render.yaml blueprint
6. Set the environment variables in the Render dashboard

### Method 2: Manual Deployment
1. Create a new Worker service on Render
2. Connect your GitHub repository
3. Configure settings:
   - **Build Command:**
     ```bash
     apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     python bot3.py
     ```
4. Set environment variables

### 🔧 Required Environment Variables
Set these in Render dashboard → Environment section:

| Variable | Description |
|----------|-------------|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Bot token from @BotFather |
| `ADMIN` | Your Telegram user ID (get from @userinfobot) |
| `DB_URL` | MongoDB connection string |
| `DB_NAME` | Database name (default: Filex) |
| `LOG_CHANNEL` | Channel ID for logs (must be negative) |

### 📦 Local Development
1. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd telegram-rename-bot
