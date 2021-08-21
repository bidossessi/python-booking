from typing import Iterable, List
import uuid
from booking.domain import repositories, models, errors


class BookingService:
    def __init__(
        self,
        resource_repo: repositories.ResourceRepository,
        booking_repo: repositories.BookingRepository,
    ) -> None:
        self.booking_repo = booking_repo
        self.resource_repo = resource_repo

    def find(
        self,
        query: repositories.BookingQuery,
        paginate: repositories.Paginate,
    ) -> repositories.Page[models.Booking]:
        return self.booking_repo.find(query, paginate=paginate)

    def create(self, booking_in: models.BookingIn) -> models.Booking:
        conflicts = self.booking_repo.find(
            repositories.BookingQuery(
                date_start=booking_in.date_start,
                date_end=booking_in.date_end,
                resource_id=booking_in.resource_id,
            )
        )
        if conflicts:
            raise errors.BookingConflict(booking_in.resource_id)
        resource = self.resource_repo.get(booking_in.resource_id)
        booking = models.Booking(
            resource_id=booking_in.resource_id,
            order_id=booking_in.order_id,
            date_start=booking_in.date_start,
            date_end=booking_in.date_end,
            tags=resource.tags,
        )
        return self.booking_repo.save(booking)
