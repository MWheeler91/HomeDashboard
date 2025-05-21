import discord
import asyncio

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
        await self.close()

def send_discord_dm(bot_token, user_id, message):
    client = DiscordBotSender(bot_token, user_id, message)
    asyncio.run(client.start(bot_token))
