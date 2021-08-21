from typing import Generic, List, Optional, TypeVar
from pydantic.dataclasses import dataclass


@dataclass
class Paginate:
    per_page: Optional[int] = None
    page: Optional[int] = None


T = TypeVar("T")


class Page(Generic[T]):
    def __init__(self, items: List[T], count: int) -> None:
        self.count: int = count
        self.items: List[T] = items

    def __bool__(self):
        return self.count > 0

    def __len__(self):
        return len(self.items)

    def __repr__(self) -> str:
        return f"<Page({self.count})>"
