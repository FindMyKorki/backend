from crud.crud_provider import CRUDProvider
from .dataclasses import Booking, UpsertBooking


crud_provider = CRUDProvider("notifications", "user_id")


class NotificationService:
    async def create_notification(self, notification: UpsertBooking, id: int = None) -> Booking:
        new_notification = await crud_provider.create(notification.model_dump(exclude="created_at"), id)

        return Booking.model_validate(new_notification)

    async def get_notification(self, id: int) -> Booking:
        notification = await crud_provider.get(id)

        return Booking.model_validate(notification)
    
    async def get_all_user_notifications(self, user_id: int) -> list[Booking]:
        notifications = await crud_provider.get_all(user_id)

        return [Booking.model_validate(notification) for notification in notifications]

    async def update_notification(self, notification: UpsertBooking, id: int = None) -> Booking:
        updated_notification = await crud_provider.update(notification.model_dump(exclude="created_at"), id)

        return Booking.model_validate(updated_notification)

    async def delete_notification(self, id: int) -> Booking:
        deleted_notification = await crud_provider.delete(id)

        return Booking.model_validate(deleted_notification)

