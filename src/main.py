from contextlib import asynccontextmanager

from fastapi import FastAPI
from aiogram import types
from fastapi.middleware.cors import CORSMiddleware

from src.bot.bot import dp
from src.repository import create_tables, add_campaign, get_campaign, get_spec_campaign
from src.schemas import CampaignSchema
from src.utils import bot
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != f"{settings.WEBHOOK_URL}/bot":
        await bot.set_webhook(f"{settings.WEBHOOK_URL}/bot", drop_pending_updates=True)
    await create_tables()
    yield
    await bot.session.close()
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

@app.post("/bot")
async def telegram_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}


@app.get("/campaigns")
async def getcampaigns(limit: int = 10, offset: int = 0):
    campaigns = await get_campaign(limit, offset)
    return campaigns


@app.get("/campaign/{campaign_id}")
async def getcampaign(campaign_id: int):
    campaign = await get_spec_campaign(campaign_id)
    return campaign


@app.post("/addcampaign")
async def addcampaign(campaign: CampaignSchema):
    await add_campaign(campaign)
    return {"ok": True}


@app.post("/addcampaigns")
async def addcampaign(campaigns: list[CampaignSchema]):
    for campaign in campaigns:
        await add_campaign(campaign)
    return {"ok": True}
