import uuid
from typing import Iterable
from booking.domain import models, repository


class BookingService:
    def __init__(self, repo: repository.BookingRepository) -> None:
        self.repo = repo

    def find(self, query: repository.BookingQuery) -> Iterable[models.Booking]:
        return self.repo.find_bookings(query)

    def create(self, booking_in: models.BookingIn) -> models.Booking:
        resource = self.repo.get_resource(booking_in.resource_id)
        booking = models.Booking(
            resource_id=booking_in.resource_id,
            order_id=booking_in.order_id,
            date_start=booking_in.date_start,
            date_end=booking_in.date_end,
            system=booking_in.system,
            tags=resource.tags,
        )
        return self.repo.create_booking(booking)

    def get(self, item_id: uuid.UUID) -> models.Booking:
        return self.repo.get_booking(item_id)

    def update(self, item_id: uuid.UUID, timeframe: models.Timeframe) -> models.Booking:
        return self.repo.update_booking(item_id, timeframe)

    def delete(self, item_id: uuid.UUID) -> models.Booking:
        return self.repo.delete_booking(item_id)
