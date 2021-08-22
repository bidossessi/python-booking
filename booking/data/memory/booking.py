import uuid
from typing import List, Optional

from booking.domain.errors import BookingNotFound
from booking.domain.models import Booking
from booking.domain.repositories import BookingQuery, BookingRepository, Page, Paginate
from booking.helpers import singleton


def _match_booking(item: Booking, query) -> bool:
    matches_date = item.intersects(query.date_start, query.date_end)
    matches_res = item.resource_id == query.resource_id if query.resource_id else True
    matches_order = item.resource_id == query.resource_id if query.resource_id else True
    matches_tags = any(x in query.tags for x in item.tags) if query.tags else True
    return all([matches_date, matches_res, matches_order, matches_tags])


@singleton
class MemoryBookingRepo(BookingRepository):
    def __init__(self) -> None:
        super().__init__()
        self.store: List[Booking] = []

    def check(self, query: BookingQuery) -> bool:
        return any(item for item in self.store if _match_booking(item, query))

    def find(
        self,
        query: BookingQuery,
        # TODO: implement poor man's pagination
        paginate: Optional[Paginate] = None,
    ) -> Page[Booking]:

        matches = [item for item in self.store if _match_booking(item, query)]
        return Page(matches, len(matches))

    def get(self, id: uuid.UUID) -> Booking:
        try:
            return next(item for item in self.store if item.id == id)
        except StopIteration:
            raise BookingNotFound(id)

    def save(self, item: Booking) -> Booking:
        try:
            match = self.get(item.id)
            self.store = [item if s == match else s for s in self.store]
        except BookingNotFound:
            self.store.append(item)
        return item

    def delete(self, id: uuid.UUID):
        item = self.get(id)
        self.store = [match for match in self.store if match is not item]
