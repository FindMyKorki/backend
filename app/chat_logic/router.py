from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from .events import manager
from core.db_connection import supabase
from .service import ChatLogicService
from datetime import datetime, timezone
import json

chat_logic_router = APIRouter(
    prefix="/chat-logic",
    tags=["Chat Logic"]
)

chat_service = ChatLogicService()


@chat_logic_router.websocket("/ws/{chat_id}")
async def chat_websocket(websocket: WebSocket, chat_id: int):
    """WebSocket for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast message to all clients in the room
            message_data = json.loads(data)

            new_message = {
                "chat_id": chat_id,
                "sender_id": message_data.get("sender_id"),
                "content": message_data.get("content"),
                "is_media": message_data.get("is_media", False),
                "is_read": False,  
                "sent_at": datetime.now(timezone.utc).isoformat(), 
            }

            result = supabase.table("messages").insert(new_message).execute()

            if not result.data:
                await websocket.send_text(json.dumps({
                    "error": "Failed to save message to the database"
                }))
                continue
            try:
                await manager.broadcast(json.dumps(new_message))
            except RuntimeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        