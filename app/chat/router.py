from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .service import save_message, subscribe_to_messages
from .dataclasses import MessageCreate
import asyncio
import json

router = APIRouter()

active_connections = {}

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    """Websocket for a given chat"""
    await websocket.accept()

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

    def broadcast_message(message):
        """sends messages to all active connections"""
        loop = asyncio.get_event_loop()
        
        message["sent_at"] = message["sent_at"]  # Timestampz in databse

        for connection in active_connections.get(chat_id, []):
            loop.create_task(connection.send_json(message))

    subscription = subscribe_to_messages(chat_id, broadcast_message)

    try:
        while True:
            data = await websocket.receive_json()
            message = MessageCreate(**data)
            saved_message = await save_message(message)
            broadcast_message(saved_message.dict())

    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)
        if not active_connections[chat_id]:
            del active_connections[chat_id]