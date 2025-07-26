import discord
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    bot_token: str
    user_id: int
    message: str

class DiscordBotSender(discord.Client):
    def __init__(self, user_id, message):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.user_id = user_id
        self.message = message
        self.success = False
        self.exception = None

    async def on_ready(self):
        try:
            user = await self.fetch_user(self.user_id)
            await user.send(self.message)
            self.success = True
        except Exception as e:
            self.exception = str(e)
        finally:
            await self.close()

@app.post("/send_dm/")
async def send_dm(request: MessageRequest):
    bot = DiscordBotSender(user_id=request.user_id, message=request.message)

    try:
        await bot.start(request.bot_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start bot: {str(e)}")

    if bot.success:
        return {"status": "success", "message": "DM sent"}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to send DM: {bot.exception}")
