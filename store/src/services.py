import json
from typing import List, Dict, Set

from fastapi import HTTPException, WebSocket
from sqlalchemy.sql import select


from .database import processed_agent_data, SessionLocal
from .models import ProcessedAgentData


subscriptions: Dict[int, Set[WebSocket]] = {}


async def send_data_to_subscribers(user_id: int, data):
    if user_id in subscriptions:
        for websocket in subscriptions[user_id]:
            await websocket.send_json(json.dumps(data))


async def create_processed_agent_data_service(
        data: List[ProcessedAgentData]
):
    if len(data) == 0:
        return

    flatten_data = [
        {
            "road_state": p_agent_data.road_state,
            "user_id": p_agent_data.agent_data.user_id,
            "x": p_agent_data.agent_data.accelerometer.x,
            "y": p_agent_data.agent_data.accelerometer.y,
            "z": p_agent_data.agent_data.accelerometer.z,
            "latitude": p_agent_data.agent_data.gps.latitude,
            "longitude": p_agent_data.agent_data.gps.longitude,
            "timestamp": p_agent_data.agent_data.timestamp,
        }
        for p_agent_data in data
    ]
    query = processed_agent_data.insert().values(flatten_data)
    with SessionLocal() as session, session.begin():
        session.execute(query)
        # Send new data to subscribers
        user_id = data[0].agent_data.user_id
        await send_data_to_subscribers(
            user_id,
            [{**d, "timestamp": d["timestamp"].isoformat()} for d in flatten_data],
        )


async def read_processed_agent_data_service(
        processed_agent_data_id: int
):
    query = select(processed_agent_data).where(
        processed_agent_data.c.id == processed_agent_data_id
    )
    with SessionLocal() as session:
        result = session.execute(query)
        if result is None:
            raise HTTPException(status_code=404, detail="ProcessedAgentData not found")

        response = dict(zip(result.keys(), result.fetchone()))
        return response


async def list_processed_agent_data_service():
    query = select(processed_agent_data)
    with SessionLocal() as session:
        results = session.execute(query)
        response = [{k: v[i] for i, k in enumerate(results.keys())} for v in results.all()]
        return response


async def update_processed_agent_data_service(
        processed_agent_data_id: int,
        data: ProcessedAgentData,
):
    agent_data = data.agent_data
    query = (
        processed_agent_data.update()
        .where(processed_agent_data.c.id == processed_agent_data_id)
        .values(
            road_state=data.road_state,
            user_id=agent_data.user_id,
            x=agent_data.accelerometer.x,
            y=agent_data.accelerometer.y,
            z=agent_data.accelerometer.z,
            latitude=agent_data.gps.latitude,
            longitude=agent_data.gps.longitude,
            timestamp=agent_data.timestamp,
        )
    )
    with SessionLocal() as session, session.begin():
        result = session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="ProcessedAgentData not found")
        return result


async def delete_processed_agent_data_service(
        processed_agent_data_id: int,
):
    query = processed_agent_data.delete().where(
        processed_agent_data.c.id == processed_agent_data_id
    )
    with SessionLocal() as session, session.begin():
        result = session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="ProcessedAgentData not found")
        return result
