from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from .events import manager
from core.db_connection import supabase
from .service import ChatLogicService
from datetime import datetime, timezone
import json
from chats.service import ChatsService 

chat_logic_router = APIRouter(
    prefix="/chat-logic",
    tags=["Chat Logic"]
)

chat_logic_service = ChatLogicService()
chat_service = ChatsService()

async def verify_user_in_chat(websocket: WebSocket, chat_id: int, user_id: str):
    try:
        result = supabase.table("chats")\
            .select("*")\
            .eq("id", chat_id)\
            .execute()

        if not result.data:
            await websocket.close(code=403)
            return

        chat = result.data[0]
        if chat["tutor_id"] != user_id and chat["student_id"] != user_id:
            await websocket.close(code=403)
            return
        if not result.data:
            print(f"User {user_id} is not part of chat {chat_id}")
            await websocket.close(code=403)
            return
    except Exception as e:
        print(f"Supabase query failed: {e}")
        await websocket.close(code=500)
        return
    
@chat_logic_router.websocket("/ws/{chat_id}")
async def chat_websocket(websocket: WebSocket, chat_id: int):
    """WebSocket for real-time chat with user verification"""
    await websocket.accept()
    user_id = websocket.query_params.get("user_id")
    if not user_id:
        await websocket.close(code=400)  
        raise HTTPException(status_code=400, detail="Missing user_id in query parameters")

    await verify_user_in_chat(websocket, chat_id, user_id)

    await manager.connect(websocket)
    try:
        previous_messages = await chat_service.get_chat_messages(chat_id, user_id)
        await websocket.send_text(json.dumps({
            "type": "previous_messages",
            "messages": [
                {
                    **message.model_dump(),
                    "sent_at": message.sent_at.isoformat()  # Konwersja datetime na string
                }
                for message in previous_messages.messages
            ]
        }))
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            new_message = {
            "chat_id": chat_id,
            "sender_id": user_id,
            "content": message_data.get("content"),
            "is_media": message_data.get("is_media", False),
            "is_read": False,
            "sent_at": datetime.now(timezone.utc).isoformat(),  # Użycie timezone.utc
        }
            supabase.table("messages").insert(new_message).execute()
            await manager.broadcast(json.dumps(new_message))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        

@chat_logic_router.post("/chats")
async def create_chat(tutor_id: str, student_id: str):
    """
    Create a new chat between a tutor and a student
    """
    try:
        new_chat = await chat_logic_service.create_chat(tutor_id, student_id)
        return {"success": True, "chat": new_chat}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))