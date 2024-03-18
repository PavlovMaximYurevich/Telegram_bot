from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Event


async def orm_add_event(session: AsyncSession, user_data: dict):
    session.add(Event(
        event_name=user_data.get('event_name'),
        event_link=user_data.get('link'),
        contact_tg=user_data.get('tg_username'),
    ))
    # Здесь надо дождаться пока во втором боте нажмут да/нет
    await session.commit()


async def orm_get_all_event(session: AsyncSession):
    queryset = select(Event)
    res = await session.execute(queryset)
    return res.scalars().all()


async def orm_get_event(session: AsyncSession, event_id: int):
    queryset = select(Event).where(Event.id == event_id)
    res = await session.execute(queryset)
    return res.scalar()


async def orm_update_status(session: AsyncSession, event_id: int, user_data):
    queryset = update(Event).where(Event.id == event_id).values(
        approved=user_data.get('approved')
        # event_name=user_data.get('event_name'),
        # event_link=user_data.get('link'),
        # contact_tg=user_data.get('tg_username')
    )
    await session.execute(queryset)
    await session.commit()


async def orm_del_event(session: AsyncSession, event_id: int):
    queryset = delete(Event).where(Event.id == event_id)
    await session.execute(queryset)
    await session.commit()
