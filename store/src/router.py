from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .models import ProcessedAgentData
from .services import create_processed_agent_data_service, read_processed_agent_data_service, \
    update_processed_agent_data_service, subscriptions, list_processed_agent_data_service, \
    delete_processed_agent_data_service

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    if user_id not in subscriptions:
        subscriptions[user_id] = set()
    subscriptions[user_id].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions[user_id].remove(websocket)


# FastAPI CRUDL endpoints

@router.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    return await create_processed_agent_data_service(data)


@router.get("/processed_agent_data/{processed_agent_data_id}")
async def read_processed_agent_data(processed_agent_data_id: int):
    return await read_processed_agent_data_service(processed_agent_data_id)


@router.get("/processed_agent_data/")
async def list_processed_agent_data():
    return await list_processed_agent_data_service()


@router.put("/processed_agent_data/{processed_agent_data_id}")
async def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    return await update_processed_agent_data_service(processed_agent_data_id, data)


@router.delete("/processed_agent_data/{processed_agent_data_id}")
async def delete_processed_agent_data(processed_agent_data_id: int):
    return await delete_processed_agent_data_service(processed_agent_data_id)
