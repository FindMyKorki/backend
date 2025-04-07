from crud.crud_provider import CRUDProvider
from .dataclasses import Booking, UpsertBooking


crud_provider = CRUDProvider("notifications")


class NotificationService:
    async def create_notification(self, notification: UpsertBooking, id: int = None) -> Booking:
        new_notification = await crud_provider.create(notification.model_dump(exclude="created_at"), id)

        return Booking.model_validate(new_notification)

    async def get_notification(self, id: int) -> Booking:
        notification = await crud_provider.get(id)

        return Booking.model_validate(notification)

    async def update_notification(self, notification: UpsertBooking, id: int = None) -> Booking:
        updated_notification = await crud_provider.update(notification.model_dump(exclude="created_at"), id)

        return Booking.model_validate(updated_notification)

    async def delete_notification(self, id: int) -> Booking:
        deleted_notification = await crud_provider.delete(id)

        return Booking.model_validate(deleted_notification)

