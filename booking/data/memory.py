import uuid
import itertools
from typing import Iterable, List

from booking.domain import errors, models, repository
from booking.helpers import singleton


def _match_booking(item: models.Booking, query) -> bool:
    matches_date = item.intersects(query.date_start, query.date_end)
    matches_res = item.resource_id == query.resource_id if query.resource_id else True
    matches_order = item.order_id == query.order_id if query.order_id else True
    matches_tags = any(x in query.tags for x in item.tags) if query.tags else True
    return all([matches_date, matches_res, matches_order, matches_tags])


def _match_resource(item: models.Resource, query) -> bool:
    matches_res = item.resource_id == query.resource_id if query.resource_id else True
    matches_ref = (
        item.reference_id == query.reference_id if query.reference_id else True
    )
    matches_tags = any(x in query.tags for x in item.tags) if query.tags else True
    return all([matches_res, matches_ref, matches_tags])


@singleton
class MemoryRepository(repository.BookingRepository):
    def __init__(self) -> None:
        super().__init__()
        self.resource_store: List[models.Resource] = []
        self.booking_store: List[models.Booking] = []

    def find_resources(
        self, query: repository.ResourceQuery
    ) -> Iterable[models.Resource]:
        return [item for item in self.resource_store if _match_resource(item, query)]

    def get_resource(self, item_id: uuid.UUID) -> models.Resource:
        try:
            return next(
                item for item in self.resource_store if item.resource_id == item_id
            )
        except StopIteration:
            raise errors.ResourceNotFound(item_id)

    def create_resource(self, item: models.Resource) -> models.Resource:
        # Emulate FK constraint
        conflict = any(
            match.reference_id == item.reference_id for match in self.resource_store
        )
        if conflict:
            raise errors.ResourceConflict(item)
        self.resource_store.append(item)
        return item

    def update_resource(self, item_id: uuid.UUID, tags: List[str]) -> models.Resource:
        match = self.get_resource(item_id)
        match.tags = tags
        return match

    def delete_resource(self, item_id: uuid.UUID):
        # Emulate FK constraint
        conflicts = any(x.resource_id == item_id for x in self.booking_store)
        if conflicts:
            raise errors.ResourceConflict(item_id)
        self.resource_store = [
            match for match in self.resource_store if match.resource_id != item_id
        ]

    def check_booking_overlap(self, item: models.Booking) -> bool:
        return any(
            match.overlaps_other(item)
            for match in self.booking_store
            if match.resource_id == item.resource_id
        )

    def find_bookings(self, query: repository.BookingQuery) -> Iterable[models.Booking]:
        return [item for item in self.booking_store if _match_booking(item, query)]

    def get_booking(self, item_id: uuid.UUID) -> models.Booking:
        try:
            return next(
                item for item in self.booking_store if item.booking_id == item_id
            )
        except StopIteration:
            raise errors.BookingNotFound(item_id)

    def create_booking(self, item: models.Booking) -> models.Booking:
        # Emulate FK constraint
        conflict = self.check_booking_overlap(item)
        if conflict:
            raise errors.BookingConflict(item)
        self.booking_store.append(item)
        return item

    def update_booking(self, item_id: uuid.UUID, timeframe: models.Timeframe):
        conflict = any(
            match.overlaps_timeframe(timeframe)
            for match in self.booking_store
            if match.booking_id == item_id
        )
        if conflict:
            raise errors.BookingConflict(item_id)
        match = self.get_booking(item_id)
        match.timeframe = timeframe
        return match

    def delete_booking(self, item_id: uuid.UUID):
        self.booking_store = [
            match for match in self.booking_store if match.booking_id != item_id
        ]

    # In-memory implementation.

    def find_free_resources(
        self, timeframe: models.Timeframe, tags: List[str] = None
    ) -> Iterable[models.Resource]:
        mached_bookings = [
            b for b in self.booking_store if b.overlaps_timeframe(timeframe)
        ]
        to_exclude = [
            k
            for k, _ in itertools.groupby(mached_bookings, key=lambda x: x.resource_id)
        ]

        def _filter(item: models.Resource) -> bool:
            matches_exclude = item.resource_id not in to_exclude
            matches_tags = any(x in tags for x in item.tags) if tags else True
            return all([matches_exclude, matches_tags])

        return list(filter(_filter, self.resource_store))
