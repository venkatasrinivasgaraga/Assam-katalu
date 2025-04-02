# CPGA Telegram Bot

A Telegram bot that responds to the `/getcpga` command with an admin-configurable message.

## Features

- Web admin panel to configure the bot message
- Telegram bot that responds to commands
- Secure admin authentication for message updates

## Available Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/getcpga` - Get CPGA information (configurable message)
- `/setcpga <message>` - Set the CPGA message (admin only)

## Setup

1. Clone this repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather
   - `ADMIN_TELEGRAM_IDS`: Comma-separated list of Telegram user IDs for admin access (optional)

4. Run the application:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

## Admin Access

The web admin panel is available at `/admin`. Default credentials:
- Username: `admin`
- Password: `admin` 

It's highly recommended to change the default password after first login.

## Security Notice

In a production environment, make sure to:
1. Change the default admin password
2. Set the `SESSION_SECRET` environment variable
3. Use HTTPS for the web interface

## License

MIT