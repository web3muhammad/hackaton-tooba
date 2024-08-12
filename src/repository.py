from sqlalchemy import select
from src.database import async_engine, Base, async_session_factory
from src.models import User, Campaign
from src.schemas import CampaignSchema


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_user(telegram_id: int, username: str, full_name: str, thread: str):
    async with async_session_factory() as session:
        session.add(User(
            id=telegram_id,
            username=username,
            full_name=full_name,
            thread=thread
            ))
        await session.commit()


async def check_user_exists(telegram_id: int):
    async with async_session_factory() as session:
        statement = select(User.id).filter_by(id=telegram_id)
        exists = await session.execute(statement)
        result = exists.scalar() is not None
        return result


async def get_user_thread(telegram_id: int):
    async with async_session_factory() as session:
        statement = select(User.thread).filter_by(id=telegram_id)
        exists = await session.execute(statement)
        result = exists.scalar()
        return result


async def add_campaign(campaign: CampaignSchema):
    async with async_session_factory() as session:
        session.add(Campaign(
            id=campaign.id,
            goal=campaign.goal,
            collected=campaign.collected,
            title=campaign.title,
            description=campaign.description
            ))
        await session.commit()

async def get_campaign(limit, offset):
    async with async_session_factory() as session:
        statement = select(Campaign).limit(limit).offset(offset)
        exists = await session.execute(statement)
        result = exists.scalars().all()
        return result

async def get_spec_campaign(campaign_id):
    async with async_session_factory() as session:
        statement = select(Campaign).filter_by(id=campaign_id)
        exists = await session.execute(statement)
        result = exists.scalars().one()
        return result
