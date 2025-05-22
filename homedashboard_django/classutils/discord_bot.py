import discord
import asyncio
from error_logging.logger import ErrorLogger

class DiscordBotSender(discord.Client):
    def __init__(self, token, user_id, message):
        super().__init__(intents=discord.Intents.default())
        self.token = token
        self.user_id = user_id
        self.message = message

    async def on_ready(self):
        try:
            user = await self.fetch_user(self.user_id)
            await user.send(self.message)
            print(f"Message sent to {user}")
        except Exception as e:
            print(f"Failed to send message: {e}")
        finally:
            await self.close()

def send_discord_dm(bot_token, user_id, message):
    try:
        client = DiscordBotSender(bot_token, user_id, message)
        client.run(bot_token)
        # asyncio.run(client.start(bot_token))
    except Exception as e:
        ErrorLogger.log(e, app="audiowatch", user=None)