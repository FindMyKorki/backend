from core.db_connection import supabase
from crud.crud_provider import CRUDProvider

from .dataclasses import UpsertSubject, Message


class MessageException(Exception):
    pass


crud_provider_message = CRUDProvider("messages")
crud_provider_chat = CRUDProvider("chats")


class SubjectService:
    async def create_message(self, message: UpsertSubject, receiver_id: str = None, id: int = None) -> Message:
        if receiver_id is None and message.chat_id is None:
            raise MessageException("Either receiver_id or chat_id must be provided")

        # If chat_id is provided, we just need to create the message
        if message.chat_id is not None:
            new_message = await crud_provider_message.create(message.model_dump(exclude="sent_at"), id)
            await self.__update_chat(message.chat_id)
            return Message.model_validate(new_message)

        if message.sender_id == receiver_id:
            raise MessageException("Sender and receiver cannot be the same")

        # If chat_id is not provided, we are checking if the chat already exists
        query = (
            supabase.table("chats")
            .select("id")
            .or_(
                f"and(student_id.eq.{message.sender_id},tutor_id.eq.{receiver_id}),and(student_id.eq.{receiver_id},tutor_id.eq.{message.sender_id})"
            )
        )

        try:
            chats = query.execute().data
        except Exception as e:
            raise MessageException(f"Error while checking if chat exists: {e}")

        # If we find a chat, we can create the message in that chat
        if len(chats) != 0:
            message.chat_id = chats[0]["id"]
            new_message = await crud_provider_message.create(message.model_dump(exclude="sent_at", exclude_none=True),
                                                             id)
            await self.__update_chat(message.chat_id)
            return Message.model_validate(new_message)

        # If we don't find a chat, we need to create a new one
        # But first we need to check if the sender is a tutor or a student
        query = (
            supabase.table("profiles")
            .select("is_tutor")
            .eq("id", message.sender_id)
        )

        try:
            profile = query.execute().data[0]
        except Exception as e:
            raise MessageException(f"Error while checking if sender is tutor, profile might not exist: {e}")

        if profile["is_tutor"]:
            raise MessageException("Tutor cannot send first message to a student")

        # If the sender is a student, we can create a new chat
        new_chat = await self.__create_chat(message.sender_id, receiver_id)
        chat_id = new_chat["id"]

        message.chat_id = chat_id
        new_message = await crud_provider_message.create(message.model_dump(exclude="sent_at", exclude_none=True), id)
        return Message.model_validate(new_message)

    async def get_message(self, id: int) -> Message:
        message = await crud_provider_message.get(id)

        return Message.model_validate(message)

    async def update_message(self, message: UpsertSubject | Message, id: int = None) -> Message:
        updated_message = await crud_provider_message.update(message.model_dump(exclude="sent_at", exclude_none=True),
                                                             id)

        await self.__update_chat(updated_message["chat_id"])
        return Message.model_validate(updated_message)

    async def delete_message(self, id: int) -> Message:
        deleted_message = await crud_provider_message.delete(id)

        await self.__update_chat(deleted_message["chat_id"])
        return Message.model_validate(deleted_message)

    async def __create_chat(self, student_id: str, tutor_id: str) -> int:
        chat = {"student_id": student_id, "tutor_id": tutor_id}

        return await crud_provider_chat.create(chat)

    async def __update_chat(self, chat_id: int) -> int:
        update = {"last_updated_at": "now()"}

        chat = await crud_provider_chat.update(update, chat_id)
        return chat
