from crud.crud_provider import CRUDProvider

from .dataclasses import BookingAttachment, UpsertBookingAttachment

crud_provider = CRUDProvider("booking_attachments")


class BookingAttachmentService:
    async def create_booking_attachment(self, booking_attachment: UpsertBookingAttachment,
                                        id: int = None) -> BookingAttachment:
        new_booking_attachment = await crud_provider.create(booking_attachment.model_dump(exclude="created_at"), id)

        return BookingAttachment.model_validate(new_booking_attachment)

    async def get_booking_attachment(self, id: int) -> BookingAttachment:
        booking_attachment = await crud_provider.get(id)

        return BookingAttachment.model_validate(booking_attachment)

    async def update_booking_attachment(self, booking_attachment: UpsertBookingAttachment,
                                        id: int = None) -> BookingAttachment:
        updated_booking_attachment = await crud_provider.update(booking_attachment.model_dump(exclude="created_at"), id)

        return BookingAttachment.model_validate(updated_booking_attachment)

    async def delete_booking_attachment(self, id: int) -> BookingAttachment:
        deleted_booking_attachment = await crud_provider.delete(id)

        return BookingAttachment.model_validate(deleted_booking_attachment)
